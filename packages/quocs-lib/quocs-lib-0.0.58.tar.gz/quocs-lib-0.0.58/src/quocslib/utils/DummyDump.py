# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright 2021-  QuOCS Team
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from quocslib.utils.AbstractDump import AbstractDump


class DummyDump(AbstractDump):
    """Dummy class for dumping the controls"""

    def __init__(self, results_path: str = ".", date_time: str = ".", dump_format: str = "npz", **kwargs):
        pass

    def dump_controls(self, pulses: list = [], timegrids: list = [], parameters: list = [], **kwargs) -> None:
        """Do Nothing"""
        pass
