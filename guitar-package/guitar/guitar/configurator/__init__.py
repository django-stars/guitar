class Question(dict):
    def __init__(self, patcher_type, configurator, **kwargs):
        self.configurator = configurator
        self.patcher_type = patcher_type

        super(Question, self).__init__(**kwargs)

        # dict answer_id => (answer_variable, answer_variable_value)
        self.answers = {}

        self.answers = dict(
            (answer['key'], (answer.get('variable') or self.get('variable'), answer.get('value')))
            for answer in self.get('answers', [])
        )

    def answer(self, answer_key):
        if self['type'] == 'input':
            variable, answer = (self['variable'], answer_key or self.get('default'))
        else:
            variable, answer = self.answers[answer_key]

        self.configurator.set_variable(self.patcher_type, variable, answer)


class Configurator(object):

    def __init__(self, config_json, file_paths):
        self.templates_data = {}
        self.config = config_json
        self.questions = []
        self.file_paths = file_paths

        for pather_config in config_json:
            template_variables = pather_config.get('variables')
            # Set place, where template data will be situated
            if template_variables:
                self.templates_data[pather_config['type']] = dict(
                    zip(template_variables, [''] * len(template_variables))
                )
            else:
                self.templates_data[pather_config['type']] = None

            # Initialize questions
            for question in pather_config.get('questions', []):
                answer_id = 0

                for answer in question.get('answers', []):
                    answer['key'] = answer_id
                    answer_id += 1

                self.questions.append(Question(pather_config['type'], self, **question))

    def __iter__(self):
        return self

    def next(self):
        if not self.questions:
            raise StopIteration

        question = self.questions.pop(0)

        if 'exclude' in question:
            exclude = False

            for excl_condition in question['exclude']:
                patcher_data = self.templates_data[question.patcher_type]
                # TODO: check exclude format
                if patcher_data.get(excl_condition['variable']) == excl_condition['value']:
                    exclude = True
                    break

            if exclude:
                return self.next()

        return question

    def set_variable(self, patcher_type, variable, value):
        self.templates_data[patcher_type][variable] = value

    def get_patches(self):
        patches = {}

        for patcher_config in self.config:
            # TODO: validation
            patch_type = patcher_config['type']

            template = patcher_config['template']

            if self.templates_data[patch_type]:
                template %= self.templates_data[patch_type]

            patches[patch_type] = {
                'patch': {
                    'item_to_add': template,
                    'before': patcher_config.get('add_before'),
                    'after': patcher_config.get('add_after')
                },
                'file_path': self.file_paths[patch_type]
            }

        return patches

    def get_template_variables(self, template):
        return [item[1] for item in Formatter().parse(template) if item]
