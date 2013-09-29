import re


class ValidationError(Exception):
    pass


class CantApplyPatch(Exception):
    pass


class ItemPatcher(object):
    def apply_patch(self, content, patch):
        """
        Write your code to apply patch to file content.
        :param content: (str) file content
        :param patch: patch objects
        """
        pass

    def apply(self, content, patch):
        new_content = self.apply_patch(content, patch)
        self.validate(new_content)

        return new_content

    def validate(self, file_obj):
        pass


class SettingsPatcher(ItemPatcher):

    def apply_patch(self, content, patch_obj):
        # Now Just add code to end of file
        #TODO: reformat code reindent.py?/?
        patch = '\n'.join(patch_obj)
        content += '\n%s\n' % patch
        return content


class ListPatcher(ItemPatcher):

    def apply_patch(self, content, patch_obj, variable_name):
        # Regular expression of list or tuple variable with open breckets
        list_start_reg = r'^%s\s*= *[\(\[]+\n*' % variable_name

        list_start = re.search(list_start_reg, content, re.M)

        if not list_start:
            raise CantApplyPatch('Cant find %s variable' % variable_name)

        list_start = list_start.group()
        # Regexp of middleware variable with list/tuple of midlewwares and start of next variable
        list_variable_reg = r'^%s\s*= *[\(\[]+\n*([^\)\]]+)([\)\]]+\n*[A-Z_0-9= ]*)' % variable_name

        try:
            list_items_str, next_variable = re.search(list_variable_reg, content, re.M).groups()
        except (AttributeError, ValueError):
            raise CantApplyPatch

        where = 'before' if patch_obj['before'] else 'after' if patch_obj['after'] else None
        if where:
            item_to_find = patch_obj[where]
        else:
            item_to_find = None

        # Append new list item before or after given list item
        item_to_append = "'%s'," % patch_obj['item_to_add']
        if item_to_find:
            list_items_str = self._append(list_items_str, item_to_find, item_to_append, where)
        else:
            list_items_str = self._append_to_end(list_items_str, item_to_append)

        first_part, last_part = content.split(next_variable)
        first_part, __ = first_part.split(list_start)

        content = ''.join([first_part, list_start, list_items_str, next_variable, last_part])

        return content

    def _append_to_end(self, list_items_str, item_to_append):
        reg = r'(\,?)[ \t]*$'

        comma = re.search(reg, list_items_str).groups()[0]

        if not comma:
            list_items_str = self._add_comma(list_items_str)

        return list_items_str + self._prepare_item_to_add(list_items_str, item_to_append)

    def _prepare_item_to_add(self, list_items_str, item_to_append):
        return self._get_identation(list_items_str) + item_to_append + '\n'

    def _add_comma(self, string):
        return re.sub(r'\n$', ',\n', string)

    def _get_identation(self, list_items_str):
        identation = re.search(r"([ \t]*)['\"]", list_items_str) or ''

        if identation:
            identation = identation.groups()[0]

        return identation

    def _append(self, list_items_str, item_to_find, item_to_append, where):
        # Regexp
        reg = r"[ \t]*'%s' *(,?)\n*" % item_to_find

        has_item = re.search(reg, list_items_str)

        if not has_item:
            list_items_str = self._append_to_end(list_items_str, item_to_append)
        else:
            item_to_append = self._prepare_item_to_add(list_items_str, item_to_append)
            item_to_find = has_item.group()
            comma = has_item.groups()[0]

            splited_list_data = list_items_str.split(item_to_find)

            # Now only append before/after first found item
            if where == 'after':
                splited_list_data[1] = item_to_append + splited_list_data[1]
            else:
                splited_list_data[0] = splited_list_data[0] + item_to_append

            if not comma:
                item_to_find = re.sub(r'\n$', ',\n', item_to_find)

            list_items_str = item_to_find.join(splited_list_data)

        return list_items_str


class MiddlewarePatcher(ListPatcher):
    def apply_patch(self, content, patch_obj):
        patch_obj['item_to_add'] = patch_obj['middleware']
        return super(MiddlewarePatcher, self).apply_patch(content, patch_obj, 'MIDDLEWARE_CLASSES')


class AppsPatcher(ListPatcher):
    def apply_patch(self, content, patch_obj):
        patch_obj['item_to_add'] = patch_obj['app']
        return super(AppsPatcher, self).apply_patch(content, patch_obj, 'INSTALLED_APPS')


class UrlsPatcher(ItemPatcher):

    def apply_patch(self, content, patch_obj):
        # Split urls.py by 'url('
        parts = content.split('url(')

        item_to_find = patch_obj.get('before') or patch_obj.get('after')
        # By default item will be added to end
        place_id_to_append = len(parts) - 1

        # If set parameter after or before what item should we add new - lets find it
        if item_to_find:
            index_where_item = None

            # Find first entry
            for i, part in enumerate(parts):
                if item_to_find in part:
                    index_where_item = i
                    break

            if index_where_item is not None:
                if patch_obj.get('before'):
                    # Select item that goes before item that we found
                    place_id_to_append = index_where_item - 1
                else:
                    place_id_to_append = index_where_item

        item_to_append = self._prepare_item_to_append(patch_obj['url'])

        if place_id_to_append == len(parts) - 1:
            # If we add in end of list, add identation before
            item_to_append = self._get_identation(content) + item_to_append
        else:
            item_to_append = item_to_append + self._get_identation(content)

        parts[place_id_to_append] = self._append_after(
            parts[place_id_to_append],
            item_to_append)

        return 'url('.join(parts)

    def _get_identation(self, content):
        reg = re.search(r'^(\s*)url\(', content, re.M)
        identation = reg.groups()[0] if reg else ''
        return identation

    def _prepare_item_to_append(self, item_to_append):
        return '%s,\n' % item_to_append

    def _has_comma(self, string):
        reg = re.search(r'(,)\s*$', string)
        has_comma = True if reg and reg.groups()[0] else False

        return has_comma

    def _append_after(self, urlpattern_item, item_to_append):
        closing_breckets_count = urlpattern_item.count(')')

        if closing_breckets_count:
            # Calculate difference between closing and opening breckets
            closing_breckets_count = closing_breckets_count - urlpattern_item.count('(')

        splited_items = urlpattern_item.split(')')

        place_to_append = splited_items[-closing_breckets_count]

        if not self._has_comma(place_to_append):
            place_to_append = re.sub('\s*$', ',\n', place_to_append)

        place_to_append += item_to_append
        splited_items[-closing_breckets_count] = place_to_append

        urlpattern_item = ')'.join(splited_items)

        return urlpattern_item
