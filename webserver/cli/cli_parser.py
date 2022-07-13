#!/usr/bin/env python
# coding=utf-8

"""
TODO
"""
import os
import sys

import click

sys.path.append(os.getcwd())

plugin_folder = os.path.join(os.path.dirname(__file__), 'plugins')

HELP_TEXT = f"""
Dorothy: This CLI is a interface to call the Dorothy server utilities. For more information about Dorothy,
see the docs: 

https://github.com/tb-brics/dorothy-image-service#readme
"""


class DorothyCLI(click.MultiCommand):

    def list_commands(self, *args, **kwargs):
        """
        Function used to get commands from plugins directory
        Returns:
            List of plugins found
        """
        plugins = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py') and filename != '__init__.py':
                plugins.append(filename.replace(".py", ""))
        plugins.sort()
        return plugins

    def get_command(self, ctx, name, **kwargs) -> callable:
        """
        This function is responsible for compile and eval each plugin found by 'list_commands' and return the respective callable.
        Args:
            ctx: Click context
            name (str): Python plugin file prefix (<name>_command.py)
            **kwargs: Extra args

        Returns:
            The callable found for that plugin
        """
        register = {}
        command_package = os.path.join(plugin_folder, name + '.py')
        with open(command_package) as file:
            code = compile(file.read(), command_package, 'exec')
            eval(code, register, register)
        if "main" not in register:
            raise RuntimeError("Invalid plugin %s_command.py: Main command not found." % name)
        return register["main"]


cli = DorothyCLI(help=HELP_TEXT)

if __name__ == '__main__':
    cli()
