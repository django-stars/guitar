class Question(dict):
    def __init__(self, patcher_type, configurator, **kwargs):
        self.configurator = configurator
        self.patcher_type = patcher_type

        super(Question, self).__init__(**kwargs)

        # dict ansver_id => (ansver_variable, ansver_variable_value)
        self.ansvers = dict(
            (ansver['key'], (ansver.get('variable') or self.get('variable'), ansver.get('value')))
            for ansver in self.get('ansvers', [])
        )

    def ansver(self, ansver_key):
        self.configurator.set_variable(self.patcher_type, *self.ansvers[ansver_key])


class Configurator(object):

    def __init__(self, config_json, file_paths):
        self.templates_data = {}
        self.config = config_json
        self.questions = []
        self.file_paths = file_paths

        for pather_config in config_json:
            # Set place, where template data will be situated
            self.templates_data[pather_config['type']] = {}

            # Initialize questions
            for question in pather_config.get('questions', []):
                self.questions.append(Question(pather_config['type'], self, **question))

    def __iter__(self):
        return self

    def next(self):
        question = self.questions.pop()

        if question['exclude']:
            exclude = False
            for excl_condition in question['exclude']:
                patcher_data = self.templates_data[question.patcher_type]
                # TODO: check exclude format
                if patcher_data.get(excl_condition['variable']) == excl_condition['value']:
                    exclude = True
                    break

        if exclude:
            return self.next()
        else:
            return question

    def set_variable(self, patcher_type, variable, value):
        self.templates_data[patcher_type][variable] = value

    def get_patches(self):
        patches = {}

        for patcher_config in self.config_json:
            # TODO: validation
            patch_type = patcher_config['type']
            template = patcher_config['template']

            patches[patch_type] = {
                'patch': {
                    'item_to_add': template % self.templates_data[patch_type],
                    'before': patcher_config.get('add_before'),
                    'after': patcher_config.get('add_after')
                },
                'file_path': self.file_paths[patch_type]
            }

        return patches
