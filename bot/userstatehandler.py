#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Ricardo Ruiz

import random


class UserStateHandler(object):
    """Manage user and states and avoid repeated states"""

    def __init__(self, filename):
        """The file must contain an state per line"""

        self._filename = open(filename, 'a+')
        self._user_states = {}
        self._tempstates = []

    @property
    def states(self):

        self._filename.seek(0)
        return self._filename.readlines()

    def add(self, state):

        new_state_line = state + '\n'
        self._filename.write(new_state_line)

    def _shuffle(self):

        self._tempstates = self.states
        random.shuffle(self._tempstates)

    def add_user(self, user):
        """Identify an user with a state_cicle"""

        self._shuffle()
        self._user_states[user] = self._tempstates

    def close(self):

        self._filename.close()

    def pop_state(self, user):

        completed = not self._user_states[user]
        if completed or not user in self._user_states:
            self.add_user(user)
        return self._user_states[user].pop()

    def __contains__(self, user):

        return user in self._user_states

    def __delitem__(self, user):

        del self._user_states[user]
