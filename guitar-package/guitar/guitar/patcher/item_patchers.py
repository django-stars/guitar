import re


class ValidationError(Exception):
    pass


class CantApplyPatch(Exception):
    pass


class ItemPatcher:
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


class MiddlewarePatcher(ItemPatcher):
    variable_name = 'MIDDLEWARE_CLASSES'

    def apply_patch(self, content, patch_obj):
        # Regular expression of middleware variable with open breckets
        mid_start_reg = r'^%s\s*= *[\(\[]+\n*' % self.variable_name

        mid_start = re.search(mid_start_reg, content, re.M)

        if not mid_start:
            raise CantApplyPatch('Cant find %s variable' % self.variable_name)

        mid_start = mid_start.group()
        # Regexp of middleware variable with list/tuple of midlewwares and start of next variable
        middleware_variable_reg = r'^%s\s*= *[\(\[]+\n*([^\)\]]+)([\)\]]+\n*[A-Z_0-9= ]*)' % self.variable_name

        try:
            middlewares, next_variable = re.search(middleware_variable_reg, content, re.M).groups()
        except (AttributeError, ValueError):
            raise CantApplyPatch

        where = 'before' if patch_obj['before'] else 'after'

        # Append middleware before or after given middleware
        middlewares = self._append(middlewares, patch_obj[where], "'%s'," % patch_obj['middleware'], where)

        first_part, last_part = content.split(next_variable)
        first_part, old_middlevares = first_part.split(mid_start)

        content = ''.join([first_part, mid_start, middlewares, next_variable, last_part])

        return content

    def _append(self, middlewares, middleware_to_find, middleware_to_append, where):
        # Regexp
        reg = r"[ \t]*'%s' *,?\n*" % middleware_to_find

        # TODO: has coma?
        has_middleware = re.search(reg, middlewares)

        identation = re.search(r"([ \t]*)['\"]", middlewares) or ''
        if identation:
            identation = identation.groups()[0]

        middleware_to_append = identation + middleware_to_append + '\n'

        if not has_middleware:
            middlewares += middleware_to_append
        else:
            middleware_to_find = has_middleware.group()

            splited_middlewares = middlewares.split(middleware_to_find)

            # Now append before/after first found middleware

            if where == 'after':
                splited_middlewares[1] = middleware_to_append + splited_middlewares[1]
            else:
                splited_middlewares[0] = splited_middlewares[0] + middleware_to_append

            middlewares = middleware_to_find.join(splited_middlewares)

        return middlewares


class AppsPatcher(ItemPatcher):
    pass


class UrlsPatcher(ItemPatcher):
    pass
