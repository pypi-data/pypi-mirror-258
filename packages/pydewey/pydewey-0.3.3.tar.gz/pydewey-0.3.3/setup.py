#!/usr/bin/env python
#   -*- coding: utf-8 -*-

from setuptools import setup
from setuptools.command.install import install as _install

class install(_install):
    def pre_install_script(self):
        pass

    def post_install_script(self):
        pass

    def run(self):
        self.pre_install_script()

        _install.run(self)

        self.post_install_script()

if __name__ == '__main__':
    setup(
        name = 'pydewey',
        version = '0.3.3',
        description = 'Dewey — a fast reproducible training automation tool for MLOps pipelines.',
        long_description = 'Dewey — a fast reproducible training automation tool for MLOps pipelines.\n\nDewey is a machine learning automation tool written to create consistent reproducible ways to train models \nin a framework agnostic way. It allows providing a training specification, and the Dewey training framework \ntakes care of all of the standard boilerplate code involving writing training loops, monitoring & metrics, \nmanaging model checkpoints, and more. Please note that this tool is in early stages of development and is \nprone to rapid updates and breaking API changes.\n',
        long_description_content_type = None,
        classifiers = [
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python'
        ],
        keywords = '',

        author = 'David Buzinski',
        author_email = 'davidbuzinski@gmail.com',
        maintainer = 'David Buzinski',
        maintainer_email = 'davidbuzinski@gmail.com',

        license = 'Apache License, Version 2.0',

        url = 'https://github.com/dbuzinski/dewey',
        project_urls = {
            'Bug Tracker': 'https://github.com/dbuzinski/dewey/issues',
            'Source Code': 'https://github.com/dbuzinski/dewey'
        },

        scripts = [
            'scripts/dwy',
            'scripts/dwy.bat'
        ],
        packages = [],
        namespace_packages = [],
        py_modules = [
            'dewey.TrainingManager',
            'dewey.cli',
            'dewey.core',
            'dewey.internal.PluginData',
            'dewey.internal.PluginManager',
            'dewey.plugins.base',
            'dewey.plugins.pytorch',
            'dewey.plugins.pytorch_checkpoints',
            'dewey.plugins.pytorch_tensorboard',
            'dewey.plugins.tensorflow',
            'dewey.plugins.tensorflow_checkpoints',
            'dewey.plugins.training_progress'
        ],
        entry_points = {},
        data_files = [],
        package_data = {},
        install_requires = [],
        extras_require = {
            'pytorch': ['torch>=2.1.0'],
            'pytorch-checkpoints': ['torch>=2.1.0'],
            'pytorch-tensorboard': ['torch>=2.1.0', 'tensorboard>=2.13.0'],
            'tensorflow': ['tensorflow>=2.13.0'],
            'tensorflow-checkpoints': ['tensorflow>=2.13.0'],
            'training-progress': ['alive-progress>=3.1.5']
        },
        dependency_links = [],
        zip_safe = True,
        cmdclass = {'install': install},
        python_requires = '>=3.8',
        obsoletes = [],
    )
