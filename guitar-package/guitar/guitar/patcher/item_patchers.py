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

        where = 'before' if patch_obj['before'] else 'after'

        # Append new list item before or after given list item
        list_items_str = self._append(list_items_str, patch_obj[where], "'%s'," % patch_obj['item_to_add'], where)

        first_part, last_part = content.split(next_variable)
        first_part, __ = first_part.split(list_start)

        content = ''.join([first_part, list_start, list_items_str, next_variable, last_part])

        return content

    def _append(self, list_items_str, item_to_find, item_to_append, where):
        # Regexp
        reg = r"[ \t]*'%s' *(,?)\n*" % item_to_find

        has_item = re.search(reg, list_items_str)

        identation = re.search(r"([ \t]*)['\"]", list_items_str) or ''
        if identation:
            identation = identation.groups()[0]

        item_to_append = identation + item_to_append + '\n'

        if not has_item:
            list_items_str += item_to_append
        else:
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
    pass
