from hidparser.UsagePage.UsagePage import UsagePage, UsageType, Usage


class GenericDesktop(UsagePage):
    pointer = Usage(0x01, UsageType.collection_physical)
    mouse = Usage(0x02, UsageType.collection_application)
    joystick = Usage(0x04, UsageType.collection_application)
    game_pad = Usage(0x05, UsageType.collection_application)
    keyboard = Usage(0x06, UsageType.collection_application)
    multi_axis_controller = Usage(0x08, UsageType.collection_application)
    tablet_pc_system_controls = Usage(0x09, UsageType.collection_application)
    x = Usage(0x30, UsageType.data_dynamic_value)
    y = Usage(0x31, UsageType.data_dynamic_value)
    z = Usage(0x32, UsageType.data_dynamic_value)
    r_x = Usage(0x33, UsageType.data_dynamic_value)
    r_y = Usage(0x34, UsageType.data_dynamic_value)
    r_z = Usage(0x35, UsageType.data_dynamic_value)
    slider = Usage(0x36, UsageType.data_dynamic_value)
    dial = Usage(0x37, UsageType.data_dynamic_value)
    wheel = Usage(0x38, UsageType.data_dynamic_value)
    hat_switch = Usage(0x39, UsageType.data_dynamic_value)
    counted_buffer = Usage(0x3A, UsageType.collection_logical)
    byte_count = Usage(0x3B, UsageType.data_dynamic_value)
    motion_wakeup = Usage(0x3C, UsageType.control_one_shot)
    start = Usage(0x3D, UsageType.control_on_off)
    select = Usage(0x3E, UsageType.control_on_off)

    v_x = Usage(0x40, UsageType.data_dynamic_value)
    v_y = Usage(0x41, UsageType.data_dynamic_value)
    v_z = Usage(0x42, UsageType.data_dynamic_value)
    v_brx = Usage(0x43, UsageType.data_dynamic_value)
    v_bry = Usage(0x44, UsageType.data_dynamic_value)
    v_brz = Usage(0x45, UsageType.data_dynamic_value)
    v_no = Usage(0x46, UsageType.data_dynamic_value)
    feature_notification = Usage(0x47, [UsageType.data_dynamic_value, UsageType.data_dynamic_flag])
    resolution_multiplier = Usage(0x48, UsageType.data_dynamic_value)

    system_control = Usage(0x80, UsageType.collection_application)
    system_power_down = Usage(0x81, UsageType.control_one_shot)
    system_sleep = Usage(0x82, UsageType.control_one_shot)
    system_wake_up = Usage(0x83, UsageType.control_one_shot)
    system_context_menu = Usage(0x84, UsageType.control_one_shot)
    system_main_menu = Usage(0x85, UsageType.control_one_shot)
    system_app_menu = Usage(0x86, UsageType.control_one_shot)
    system_menu_help = Usage(0x87, UsageType.control_one_shot)
    system_menu_exit = Usage(0x88, UsageType.control_one_shot)
    system_menu_select = Usage(0x89, UsageType.control_one_shot)
    system_menu_right = Usage(0x8A, UsageType.control_re_trigger)
    system_menu_left = Usage(0x8B, UsageType.control_re_trigger)
    system_menu_up = Usage(0x8C, UsageType.control_re_trigger)
    system_menu_down = Usage(0x8D, UsageType.control_re_trigger)
    system_cold_restart = Usage(0x8E, UsageType.control_one_shot)
    system_warm_restart = Usage(0x8F, UsageType.control_one_shot)
    d_pad_up = Usage(0x90, UsageType.control_on_off)
    d_pay_down = Usage(0x91, UsageType.control_on_off)
    d_pad_right = Usage(0x92, UsageType.control_on_off)
    d_pad_left = Usage(0x93, UsageType.control_on_off)

    system_dock = Usage(0xA0, UsageType.control_one_shot)
    system_undock = Usage(0xA1, UsageType.control_one_shot)
    system_setup = Usage(0xA2, UsageType.control_one_shot)
    system_break = Usage(0xA3, UsageType.control_one_shot)
    system_debugger_break = Usage(0xA4, UsageType.control_one_shot)
    application_break = Usage(0xA5, UsageType.control_one_shot)
    application_debugger_break = Usage(0xA6, UsageType.control_one_shot)
    system_speaker_mute = Usage(0xA7, UsageType.control_one_shot)
    system_hibernate = Usage(0xA8, UsageType.control_one_shot)

    system_display_invert = Usage(0xB0, UsageType.control_one_shot)
    system_display_internal = Usage(0xB1, UsageType.control_one_shot)
    system_display_external = Usage(0xB2, UsageType.control_one_shot)
    system_display_both = Usage(0xB3, UsageType.control_one_shot)
    system_display_dual = Usage(0xB4, UsageType.control_one_shot)
    system_display_toggle_int_ext = Usage(0xB5, UsageType.control_one_shot)
    system_display_swap_primary_secondary = Usage(0xB6, UsageType.control_one_shot)
    system_display_lcd_autoscale = Usage(0xB7, UsageType.control_one_shot)

    @classmethod
    def _get_usage_page_index(cls):
        return 0x01