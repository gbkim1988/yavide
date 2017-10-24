import logging
from common.yavide_utils import YavideUtils

class VimIndexer(object):
    def __init__(self, yavide_instance):
        self.yavide_instance = yavide_instance
        self.op = {
            0x0 : self.__run_on_single_file,
            0x1 : self.__run_on_directory,
            0x2 : self.__drop_single_file,
            0x3 : self.__drop_all,
            0x10 : self.__find_all_references
        }

    def __call__(self, op_id, args):
        self.op.get(op_id, self.__unknown_op)(args)

    def __unknown_op(self, args):
        logging.error("Unknown operation triggered! Valid operations are: {0}".format(self.op))

    def __run_on_single_file(self, args):
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeIndexer_RunOnSingleFileCompleted()")

    def __run_on_directory(self, args):
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeIndexer_RunOnDirectoryCompleted()")

    def __drop_single_file(self, args):
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeIndexer_DropSingleFileCompleted()")

    def __drop_all(self, args):
        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeIndexer_DropAllCompleted()")

    def __find_all_references(self, args):
        other_args, cursor_display_name, references = args
        quickfix_list = []
        for ref in references:
            quickfix_list.append(
                "{'filename': '" + str(ref[0]) + "', " +
                "'lnum': '" + str(ref[2]) + "', " +
                "'col': '" + str(ref[3]) + "', " +
                "'type': 'I', " +
                "'text': '" + str(cursor_display_name) + "'}" # TODO Put something more meaningful here, i.e. the corresponding source code line
            )

        YavideUtils.call_vim_remote_function(self.yavide_instance, "Y_SrcCodeIndexer_FindAllReferencesCompleted(" + str(quickfix_list).replace('"', r"") + ")")
        logging.debug("References: " + str(quickfix_list))
