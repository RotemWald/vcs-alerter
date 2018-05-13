import unittest
import datetime as dt
import message_info as mi
from alerter import alerter as alt
from message_info import MessageType
from message_tag import MessageTag
from critical_moment import CriticalMoment


class AlerterTest(unittest.TestCase):
    def setUp(self):
        self.alerter = alt.Alerter()

    def test_ds_alert(self):
        msg_info_1 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_DS, 0, 0, dt.datetime(2018, 3, 17, 16, 41, 0))

        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.DS, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.DS, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.DS, "ERROR"

    def test_tec_alert_for_group(self):
        msg_info_1 = mi.MessageInfo(MessageTag.TEC, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 41, 0))
        msg_info_2 = mi.MessageInfo(MessageTag.TEC, MessageType.TEXT, 0, 1, dt.datetime(2018, 3, 17, 16, 41, 0))
        msg_info_3 = mi.MessageInfo(MessageTag.TEC, MessageType.TEXT, 0, 2, dt.datetime(2018, 3, 17, 16, 41, 0))

        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_3) is CriticalMoment.TEC, "ERROR"

    def test_tec_alert_for_user(self):
        msg_info_1 = mi.MessageInfo(MessageTag.TEC, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 41, 0))
        msg_info_2 = mi.MessageInfo(MessageTag.TEC, MessageType.TEXT, 0, 1, dt.datetime(2018, 3, 17, 16, 41, 0))

        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.TEC, "ERROR"

    def test_nmd_alert_for_group(self):
        # message just opening the room
        msg_info_0 = mi.MessageInfo(MessageTag.MAT, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 35, 0))

        msg_info_1 = mi.MessageInfo(MessageTag.NMD, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 41, 0))
        msg_info_2 = mi.MessageInfo(MessageTag.NMD, MessageType.TEXT, 0, 1, dt.datetime(2018, 3, 17, 16, 41, 0))
        msg_info_3 = mi.MessageInfo(MessageTag.NMD, MessageType.TEXT, 0, 2, dt.datetime(2018, 3, 17, 16, 41, 0))
        msg_info_4 = mi.MessageInfo(MessageTag.NONE, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 41, 0))

        assert self.alerter.handle_message_tag(msg_info_0) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_3) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_4) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_4) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_4) is CriticalMoment.NMD, "ERROR"

    def test_nmd_alert_for_user(self):
        msg_info_1 = mi.MessageInfo(MessageTag.NMD, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 41, 0))
        msg_info_2 = mi.MessageInfo(MessageTag.NMD, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 46, 1))

        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NMD, "ERROR"

    def test_no_idleness_when_all_users_disconnect(self):
        msg_info_1 = mi.MessageInfo(MessageTag.NONE, MessageType.USER_CONNECT, 0, 0,
                                    dt.datetime(2018, 3, 17, 16, 41, 0))

        # this message opens the room
        msg_info_2 = mi.MessageInfo(MessageTag.MAT, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 42, 0))

        msg_info_3 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_IDLENESS, 0, 0,
                                    dt.datetime(2018, 3, 17, 16, 47, 1))

        msg_info_4 = mi.MessageInfo(MessageTag.NONE, MessageType.USER_DISCONNECT, 0, 0, dt.datetime(2018, 3, 17, 16, 48, 0))

        msg_info_5 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_IDLENESS, 0, 0,
                                    dt.datetime(2018, 3, 17, 16, 55, 0))

        msg_info_6 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_IDLENESS, 0, 0,
                                    dt.datetime(2018, 3, 17, 16, 55, 30))

        msg_info_7 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_IDLENESS, 0, 0,
                                    dt.datetime(2018, 3, 17, 16, 56, 0))

        msg_info_8 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_IDLENESS, 0, 0,
                                    dt.datetime(2018, 3, 17, 16, 56, 30))

        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.check_idleness_for_test(msg_info_3.room_id,
                                                    msg_info_3.timestamp) is CriticalMoment.IDLENESS, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_4) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.check_idleness_for_test(msg_info_5.room_id,
                                                    msg_info_5.timestamp) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.check_idleness_for_test(msg_info_6.room_id,
                                                    msg_info_6.timestamp) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.check_idleness_for_test(msg_info_7.room_id,
                                                    msg_info_7.timestamp) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.check_idleness_for_test(msg_info_8.room_id,
                                                    msg_info_8.timestamp) is CriticalMoment.NONE, "ERROR"

    def test_idleness_text_alert_for_group(self):
        msg_info_1 = mi.MessageInfo(MessageTag.MAT, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 35, 0))
        # no idleness in this message since five minutes have not passed
        msg_info_2 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_IDLENESS, 0, 0, dt.datetime(2018, 3, 17, 16, 39, 0))
        msg_info_3 = mi.MessageInfo(MessageTag.MAT, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 39, 0))
        msg_info_4 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_IDLENESS, 0, 0, dt.datetime(2018, 3, 17, 16, 42, 1))

        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.check_idleness_for_test(msg_info_2.room_id, msg_info_2.timestamp) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_3) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.check_idleness_for_test(msg_info_4.room_id, msg_info_4.timestamp) is CriticalMoment.IDLENESS, "ERROR"

    def test_no_idleness_no_messages(self):
        msg_info_1 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_IDLENESS, 0, 0, dt.datetime(2018, 3, 17, 16, 44, 1))

        assert self.alerter.check_idleness_for_test(msg_info_1.room_id, msg_info_1.timestamp) is CriticalMoment.NONE, "ERROR"

    def test_idleness_drag_alert_for_group(self):
        msg_info_1 = mi.MessageInfo(MessageTag.NONE, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 41, 0))
        msg_info_2 = mi.MessageInfo(MessageTag.NONE, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 44, 0))
        msg_info_3 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_IDLENESS, 0, 0, dt.datetime(2018, 3, 17, 16, 45, 0))
        msg_info_4 = mi.MessageInfo(MessageTag.NONE, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 47, 0))
        msg_info_5 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_IDLENESS, 0, 0, dt.datetime(2018, 3, 17, 16, 48, 1))

        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.check_idleness_for_test(msg_info_3.room_id, msg_info_3.timestamp) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_4) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.check_idleness_for_test(msg_info_5.room_id, msg_info_5.timestamp) is CriticalMoment.IDLENESS, "ERROR"

    def test_idleness_alert_for_user(self):
        msg_info_1 = mi.MessageInfo(MessageTag.NONE, MessageType.USER_CONNECT, 0, 0, dt.datetime(2018, 3, 17, 16, 41, 0))
        msg_info_2 = mi.MessageInfo(MessageTag.MAT, MessageType.TEXT, 0, 1, dt.datetime(2018, 3, 17, 16, 41, 0))
        msg_info_3 = mi.MessageInfo(MessageTag.MAT, MessageType.TEXT, 0, 1, dt.datetime(2018, 3, 17, 16, 44, 0))
        msg_info_4 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_IDLENESS, 0, 0, dt.datetime(2018, 3, 17, 16, 45, 0))
        msg_info_5 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_IDLENESS, 0, 0, dt.datetime(2018, 3, 17, 16, 46, 30))

        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_3) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.check_idleness_for_test(msg_info_4.room_id, msg_info_4.timestamp) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.check_idleness_for_test(msg_info_5.room_id, msg_info_5.timestamp) is CriticalMoment.IDLENESS, "ERROR"

    def test_no_idleness_after_user_disconnects(self):
        msg_info_1 = mi.MessageInfo(MessageTag.NONE, MessageType.USER_CONNECT, 0, 0,
                                    dt.datetime(2018, 3, 17, 16, 41, 0))
        msg_info_2 = mi.MessageInfo(MessageTag.NONE, MessageType.USER_CONNECT, 0, 1,
                                    dt.datetime(2018, 3, 17, 16, 41, 1))

        # this message opens the room
        msg_info_3 = mi.MessageInfo(MessageTag.MAT, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 42, 0))

        msg_info_4 = mi.MessageInfo(MessageTag.NONE, MessageType.USER_DISCONNECT, 0, 1, dt.datetime(2018, 3, 17, 16, 43, 0))

        # this is a message for not getting idleness from this user
        msg_info_5 = mi.MessageInfo(MessageTag.MAT, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 45, 00))

        msg_info_6 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_IDLENESS, 0, 0, dt.datetime(2018, 3, 17, 16, 47, 30))

        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_3) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_4) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_5) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.check_idleness_for_test(msg_info_6.room_id, msg_info_6.timestamp) is CriticalMoment.NONE, "ERROR"

    def test_tec_alert_more_important_than_nmd_alert(self):
        msg_info_1 = mi.MessageInfo(MessageTag.NMD, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 35, 0))
        msg_info_2 = mi.MessageInfo(MessageTag.TEC, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 40, 1))

        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.TEC, "ERROR"

    def test_tec_alert_not_sent_when_there_is_alert_before_it(self):
        msg_info_1 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_DS, 0, 0, dt.datetime(2018, 3, 17, 16, 35, 0))
        msg_info_2 = mi.MessageInfo(MessageTag.TEC, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 38, 00))

        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.DS, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.NONE, "ERROR"

    def test_nmd_alert_not_sent_when_there_is_alert_before_it(self):
        msg_info_1 = mi.MessageInfo(MessageTag.MAT, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 32, 59))
        msg_info_2 = mi.MessageInfo(MessageTag.NONE, MessageType.CHECK_DS, 0, 0, dt.datetime(2018, 3, 17, 16, 35, 0))
        msg_info_3 = mi.MessageInfo(MessageTag.NMD, MessageType.TEXT, 0, 0, dt.datetime(2018, 3, 17, 16, 38, 00))

        assert self.alerter.handle_message_tag(msg_info_1) is CriticalMoment.NONE, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_2) is CriticalMoment.DS, "ERROR"
        assert self.alerter.handle_message_tag(msg_info_3) is CriticalMoment.NONE, "ERROR"


if __name__ == '__main__':
    unittest.main()
