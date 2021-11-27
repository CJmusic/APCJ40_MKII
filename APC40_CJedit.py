#Embedded file name: /Users/versonator/Jenkins/live/output/Live/mac_64_static/Release/python-bundle/MIDI Remote Scripts/APC40_MkII/APC40_MkII.py
from __future__ import absolute_import, print_function, unicode_literals
from builtins import range
from functools import partial
from contextlib import contextmanager
import sys

from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ComboElement import ComboElement, DoublePressElement, MultiElement, DoublePressContext
from _Framework.ControlSurface import OptimizedControlSurface
from _Framework.Layer import Layer
from _Framework.ModesComponent import ModesComponent, ImmediateBehaviour, DelayMode, AddLayerMode, EnablingModesComponent
from _Framework.Resource import PrioritizedResource
from _Framework.SessionRecordingComponent import SessionRecordingComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.ClipCreator import ClipCreator
from _Framework.Util import const, recursive_map

from _Framework.BackgroundComponent import BackgroundComponent, ModifierBackgroundComponent
from _Framework.SubjectSlot import subject_slot
from _Framework.Dependency import inject


from _APC.APC import APC
from _APC.DeviceComponent import DeviceComponent
from _APC.DeviceBankButtonElement import DeviceBankButtonElement
from _APC.DetailViewCntrlComponent import DetailViewCntrlComponent
# from _APC.SessionComponent import SessionComponent
from _APC.ControlElementUtils import make_button, make_encoder, make_slider, make_ring_encoder, make_pedal_button
from _APC.ControlElementUtils import make_button as make_crossfade_button
from _APC.SkinDefault import make_rgb_skin, make_default_skin, make_stop_button_skin, make_crossfade_button_skin
from ._resources import Colors
from ._resources.BankToggleComponent import BankToggleComponent
from ._resources.MixerComponent import MixerComponent
from ._resources.QuantizationComponent import QuantizationComponent
from ._resources.TransportComponent import TransportComponent


from ._resources import Colors, consts
from ._resources.BankToggleComponent import BankToggleComponent
from ._resources.MixerComponent import MixerComponent
from ._resources.QuantizationComponent import QuantizationComponent
from ._resources.TransportComponent import TransportComponent
from ._resources.CustomSessionComponent import CustomSessionComponent
from ._resources.SkinDefault import make_default_skin as make_custom_skin
from ._resources.ButtonSliderElement import ButtonSliderElement

from ._resources.NoteRepeatComponent import NoteRepeatComponent
from ._resources.StepSeqComponent import StepSeqComponent, DrumGroupFinderComponent
# from .resources.CustomStepSeqComponent import StepSeqComponent, DrumGroupFinderComponent
from ._resources.GridResolution import GridResolution
from ._resources.PlayheadElement import PlayheadElement
from ._resources.MelodicComponent import MelodicComponent
from ._resources.ControlElementUtils import make_button, make_ring_encoder
from ._resources.MatrixMaps import FEEDBACK_CHANNELS
from ._resources.CustomModesComponent import CustomReenterBehaviour
from ._resources.NoteSettings import NoteEditorSettingsComponent


from ._resources import ControlElementUtils
from ._resources import SkinDefault
# from .resources import SessionComponent


from ._resources.SessionComponent import SessionComponent

from ._resources.ButtonSliderElement import ButtonSliderElement
from ._resources.AutoArmComponent import AutoArmComponent
from ._resources.DrumGroupComponent import DrumGroupComponent
from ._resources.ButtonElement import ButtonElement
from ._resources.DrumGroupComponent import DrumGroupComponent

from ._resources.VUMeters import VUMeters

# from ableton.v2.control_surface.components import UndoRedoComponent

sys.modules['_APC.ControlElementUtils'] = ControlElementUtils
sys.modules['_APC.SkinDefault'] = SkinDefault
sys.modules['_APC.SessionComponent'] = SessionComponent

from ._resources.ActionsComponent import ActionsComponent


# from _default. import Colors
# from _default.BankToggleComponent import BankToggleComponent
# from _default.MixerComponent import MixerComponent
# from _default.QuantizationComponent import QuantizationComponent
# from _default.TransportComponent import TransportComponent

# from .StepSeqComponent import StepSeqComponent
from _Framework.Control import ButtonControl

NUM_TRACKS = 8
NUM_SCENES = 5



from _Framework.Control import ButtonControl
from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import MIDI_NOTE_TYPE, MIDI_CC_TYPE
from _Framework.SubjectSlot import subject_slot

from ._resources.ActionsComponent import ActionsComponent
from ._resources.CustomSessionComponent import CustomSessionComponent
from ._resources.MatrixModesComponent import MatrixModesComponent
from ._resources.ShiftableSelectorComponent import ShiftableSelectorComponent
from ._resources.StepSequencerComponent import StepSequencerComponent
from ._resources.ConfigurableButtonElement import ConfigurableButtonElement 

from ._resources.VUMeters import VUMeters



#~~~~~~~~~~ CURRENT BUGS ~~~~~~~~~~~~~~

# ```
#  - Wont start in pan/session mode 
# looks like the background is enabled

#  - wont switch to user mode cleanly 
# needs to switch to VU mode first then it goes smooth
# seems that VU mode is related to user mode somehow 

#  - scene launch buttons are always coloured 
#  - playhead isnt working 
#  - loop selector isnt working 

# It looks like 

#  - navigation buttons in vu mode not working
#  - buttons lit on disconnect
#  - somethings weird with the stop buttons
# ```


class APC40_CJedit(APC, OptimizedControlSurface):

    def __init__(self, *a, **k):
        super(APC40_CJedit, self).__init__(*a, **k)
        self._color_skin = make_rgb_skin()
        self._default_skin = make_default_skin()
        self._stop_button_skin = make_stop_button_skin()
        self._crossfade_button_skin = make_crossfade_button_skin()
        # self._crossfade_button_skin = None
        self._double_press_context = DoublePressContext()
        self._shift_button = None
        # self._undo_button = None
        # self._redo_button = None

        self._implicit_arm = True # Set to True to auto arm the selected track
        with self.component_guard():
            self._create_controls() #controls seem to all be working
            self._create_bank_toggle()

            self._create_actions()


            self._create_mixer() #the lights aren't working for the crossfader buttons
            self._create_transport() #the shift controls aren't working for nudge
            self._create_view_control()
            self._create_quantization_selection()
            self._create_recording()

            self._skin = make_custom_skin() # is this working ?
            self._clip_creator = ClipCreator()

            self._create_background()
            # self._create_instrument() #this isn't switching to cleanly
            self._create_drum_component()
            self._create_step_sequencer() #this isn't working at all
            # self._init_note_repeat() #this is always on the toggle isn't working
            # self._init_VUMeters()

            self._create_session()
            self._session.set_mixer(self._mixer)

            self._create_vu()
            self._create_vu_controls()
            self._create_matrix_modes()

            # self._init_matrix_modes()
            self._create_device()

            # self._create_undo_redo #isn't working
            self.set_feedback_channels(FEEDBACK_CHANNELS)

        self.set_highlighting_session_component(self._session)
        self.set_device_component(self._device)
        self._matrix_background.set_enabled(False)
        self._encoder_mode.selected_mode = 'pan'
        self._matrix_modes.selected_mode = 'disable'
        self._matrix_modes.selected_mode = 'VU'
        self._matrix_modes.selected_mode = 'user'
        self._matrix_modes.selected_mode = 'session'

        self._matrix_modes.subject = self._step_sequencer
        self._matrix_modes.subject = self._vu
        self._matrix_modes.subject = self._session



    def _with_shift(self, button):
        return ComboElement(button, modifiers=[self._shift_button])

    def _create_controls(self):
        make_on_off_button = partial(make_button, skin=self._default_skin)

        def make_color_button(*a, **k):
            button = make_button(skin=self._color_skin, *a, **k)
            button.is_rgb = True
            button.num_delayed_messages = 2
            return button 

        def make_matrix_button(track, scene):
            return make_color_button(0, 32 + track - NUM_TRACKS * scene, name='%d_Clip_%d_Button' % (track, scene))

        def make_stop_button(track, prior=False):
            butt = make_button(track, 52, name='%d_Stop_Button' % track, skin=self._stop_button_skin)

            if prior:
                butt.resource_type = PrioritizedResource

            return butt

        self._shift_button = make_button(0, 98, name='Shift_Button', resource_type=PrioritizedResource)
        self._bank_button = make_on_off_button(0, 103, name='Bank_Button')
        self._left_button = make_button(0, 97, name='Bank_Select_Left_Button')
        self._right_button = make_button(0, 96, name='Bank_Select_Right_Button')
        self._up_button = make_button(0, 94, name='Bank_Select_Up_Button')
        self._down_button = make_button(0, 95, name='Bank_Select_Down_Button')

        self._stop_buttons_raw = [make_stop_button(track) for track in range(NUM_TRACKS)]
        self._stop_buttons = ButtonMatrixElement(rows=[self._stop_buttons_raw])

        self._shifted_stop_buttons = ButtonMatrixElement(rows=[
         [ self._with_shift(button) for button in self._stop_buttons_raw
         ]])

        self._stop_all_button = make_button(0, 81, name='Stop_All_Clips_Button')
        self._scene_launch_buttons_raw = [ make_color_button(0, scene + 82, name='Scene_%d_Launch_Button' % scene) for scene in range(NUM_SCENES)
                                         ]
        self._scene_launch_buttons = ButtonMatrixElement(rows=[
         self._scene_launch_buttons_raw])
        self._scene_launch_buttons.resource_type = PrioritizedResource

        self._matrix_rows_raw = [ [ make_matrix_button(track, scene) for track in range(NUM_TRACKS) ] for scene in range(NUM_SCENES)
                                ]
        self._session_matrix = ButtonMatrixElement(rows=self._matrix_rows_raw)
        self._pan_button = make_on_off_button(0, 87, name='Pan_Button', resource_type=PrioritizedResource)
        self._sends_button = make_on_off_button(0, 88, name='Sends_Button', resource_type=PrioritizedResource)
        self._user_button = make_on_off_button(0, 89, name='User_Button', resource_type=PrioritizedResource)
        self._mixer_encoders = ButtonMatrixElement(rows=[
         [ make_ring_encoder(48 + track, 56 + track, name='Track_Control_%d' % track) for track in range(NUM_TRACKS)
         ]])
        self._volume_controls = ButtonMatrixElement(rows=[
         [ make_slider(track, 7, name='%d_Volume_Control' % track) for track in range(NUM_TRACKS)
         ]])
        self._master_volume_control = make_slider(0, 14, name='Master_Volume_Control')
        self._prehear_control = make_encoder(0, 47, name='Prehear_Volume_Control')
        self._crossfader_control = make_slider(0, 15, name='Crossfader')
        self._raw_select_buttons = [ make_on_off_button(channel, 51, name='%d_Select_Button' % channel) for channel in range(NUM_TRACKS)
                                   ]
        self._arm_buttons = ButtonMatrixElement(rows=[
         [ make_on_off_button(channel, 48, name='%d_Arm_Button' % channel) for channel in range(NUM_TRACKS)
         ]])
        self._solo_buttons = ButtonMatrixElement(rows=[
         [ make_on_off_button(channel, 49, name='%d_Solo_Button' % channel) for channel in range(NUM_TRACKS)
         ]])
        self._mute_buttons = ButtonMatrixElement(rows=[
         [ make_on_off_button(channel, 50, name='%d_Mute_Button' % channel) for channel in range(NUM_TRACKS)
         ]])
        # self._crossfade_buttons = ButtonMatrixElement(rows=[
        #  [ make_button(channel, 66, name='%d_Crossfade_Button' % channel, skin=self._crossfade_button_skin) for channel in range(NUM_TRACKS)
        #  ]])
        self._crossfade_buttons = ButtonMatrixElement(rows=[[ make_crossfade_button(channel, 66, name=u'%d_Crossfade_Button' % channel, skin=self._crossfade_button_skin) for channel in range(NUM_TRACKS) ]]) ###changed to make_crossfade_button -CJ 2021-11-19
        self._select_buttons = ButtonMatrixElement(rows=[
         self._raw_select_buttons])
        self._master_select_button = make_on_off_button(channel=0, identifier=80, name='Master_Select_Button')
        self._send_select_buttons = ButtonMatrixElement(rows=[
         [ ComboElement(button, modifiers=[self._sends_button]) for button in self._raw_select_buttons
         ]])
        self._quantization_buttons = ButtonMatrixElement(rows=[
         [ ComboElement(button, modifiers=[self._shift_button]) for button in self._raw_select_buttons
         ]])
        self._metronome_button = make_on_off_button(0, 90, name='Metronome_Button')
        self._play_button = make_on_off_button(0, 91, name='Play_Button')
        self._record_button = make_on_off_button(0, 93, name='Record_Button')
        self._session_record_button = make_on_off_button(0, 102, name='Session_Record_Button')
        self._nudge_down_button = make_button(0, 100, name='Nudge_Down_Button')
        self._nudge_up_button = make_button(0, 101, name='Nudge_Up_Button')
        self._tap_tempo_button = make_button(0, 99, name='Tap_Tempo_Button')
        self._tempo_control = make_encoder(0, 13, name='Tempo_Control')
        # self._device_controls = ButtonMatrixElement(rows=[[ make_ring_encoder(16 + index, 24 + index, handler=self.value_changed, name='Device_Control_%d' % index) for index in range(8)]])
        self._device_controls = ButtonMatrixElement(rows=[[ make_ring_encoder(16 + index, 24 + index, name=u'Device_Control_%d' % index) for index in range(8) ]])
        self._device_control_buttons_raw = [ make_on_off_button(0, 58 + index) for index in range(8)
                                           ]
        self._device_bank_buttons = ButtonMatrixElement(rows=[
         [ DeviceBankButtonElement(button, modifiers=[self._shift_button]) for button in self._device_control_buttons_raw
         ]])
        self._device_prev_bank_button = self._device_control_buttons_raw[2]
        self._device_prev_bank_button.name = 'Device_Prev_Bank_Button'
        self._device_next_bank_button = self._device_control_buttons_raw[3]
        self._device_next_bank_button.name = 'Device_Next_Bank_Button'
        self._device_on_off_button = self._device_control_buttons_raw[4]
        self._device_on_off_button.name = 'Device_On_Off_Button'
        self._device_lock_button = self._device_control_buttons_raw[5]
        self._device_lock_button.name = 'Device_Lock_Button'
        self._prev_device_button = self._device_control_buttons_raw[0]
        self._prev_device_button.name = 'Prev_Device_Button'
        self._next_device_button = self._device_control_buttons_raw[1]
        self._next_device_button.name = 'Next_Device_Button'
        self._clip_device_button = self._device_control_buttons_raw[6]
        self._clip_device_button.name = 'Clip_Device_Button'
        self._detail_view_button = self._device_control_buttons_raw[7]
        self._detail_view_button.name = 'Detail_View_Button'
        self._foot_pedal_button = DoublePressElement(make_pedal_button(64, name='Foot_Pedal'))
        self._shifted_matrix = ButtonMatrixElement(rows=recursive_map(self._with_shift, self._matrix_rows_raw))
        self._shifted_scene_buttons = ButtonMatrixElement(rows=[
         [ self._with_shift(button) for button in self._scene_launch_buttons_raw
         ]])

        self._grid_resolution = GridResolution()
        # self._velocity_slider = ButtonSliderElement(tuple(self._scene_launch_buttons_raw[::-1]))
        self._velocity_slider = ButtonSliderElement(tuple(self._scene_launch_buttons_raw[::-1]))
        self._velocity_slider.resource_type = PrioritizedResource
        double_press_rows = recursive_map(DoublePressElement, self._matrix_rows_raw)
        self._double_press_matrix = ButtonMatrixElement(name='Double_Press_Matrix', rows=double_press_rows)
        self._double_press_event_matrix = ButtonMatrixElement(name='Double_Press_Event_Matrix',
                                                              rows=recursive_map(lambda x: x.double_press,
                                                                                 double_press_rows))
        self._playhead = PlayheadElement(self._c_instance.playhead)

        self._undo_button = self._with_shift(self._device_control_buttons_raw[6])
        self._undo_button.name = 'Undo_Button'
        self._redo_button = self._with_shift(self._device_control_buttons_raw[7])
        self._redo_button.name = 'Redo_Button'



    def _create_bank_toggle(self):
        self._bank_toggle = BankToggleComponent(is_enabled=False, layer=Layer(bank_toggle_button=self._bank_button))


    def _create_actions(self): 
            self._undo_button= self._with_shift(self._clip_device_button)
            self._redo_button= self._with_shift(self._detail_view_button)
            self._capture_midi_button = self._with_shift(self._record_button)

            self._actions_component = ActionsComponent(
                name='Global_Actions', 
                is_enabled=False, 
                layer=Layer(
                    # duplicate_button=self._midimap['Duplicate_Button'],
                    # double_button=self._midimap['Double_Loop_Button'],
                    # quantize_button=self._midimap['Quantize_Button']
                    undo_button= self._undo_button,
                    redo_button= self._redo_button,
                    capture_midi_button=self._capture_midi_button
                )
            )



    def _create_session(self):

        def when_bank_on(button):
            return self._bank_toggle.create_toggle_element(on_control=button)

        def when_bank_off(button):
            return self._bank_toggle.create_toggle_element(off_control=button)

        self._session = CustomSessionComponent(NUM_TRACKS, NUM_SCENES, auto_name=True, is_enabled=False,
                                                enable_skinning=True,
                                                layer=Layer(track_bank_left_button=when_bank_off(self._left_button),
                                                            track_bank_right_button=when_bank_off(self._right_button),
                                                            scene_bank_up_button=when_bank_off(self._up_button),
                                                            scene_bank_down_button=when_bank_off(self._down_button),
                                                            page_left_button=when_bank_on(self._left_button),
                                                            page_right_button=when_bank_on(self._right_button),
                                                            page_up_button=when_bank_on(self._up_button),
                                                            page_down_button=when_bank_on(self._down_button),
                                                            stop_track_clip_buttons=self._stop_buttons,
                                                            stop_all_clips_button=self._stop_all_button,
                                                            scene_launch_buttons=self._scene_launch_buttons,
                                                            clip_launch_buttons=self._session_matrix))

        clip_color_table = Colors.LIVE_COLORS_TO_MIDI_VALUES.copy()
        clip_color_table[16777215] = 119
        self._session.set_rgb_mode(clip_color_table, Colors.RGB_COLOR_TABLE)
        self._session_zoom = SessionZoomingComponent(self._session, name='Session_Overview', enable_skinning=True, is_enabled=False, layer=Layer(button_matrix=self._shifted_matrix, nav_left_button=self._with_shift(self._left_button), nav_right_button=self._with_shift(self._right_button), nav_up_button=self._with_shift(self._up_button), nav_down_button=self._with_shift(self._down_button), scene_bank_buttons=self._shifted_scene_buttons))
        self._session.set_delete_button(self._nudge_down_button)
        self._session.set_copy_button(self._nudge_up_button)



    def _create_mixer(self):
        self._mixer = MixerComponent(NUM_TRACKS, auto_name=True, is_enabled=False, invert_mute_feedback=True, layer=Layer(volume_controls=self._volume_controls, arm_buttons=self._arm_buttons, solo_buttons=self._solo_buttons, mute_buttons=self._mute_buttons, shift_button=self._shift_button, track_select_buttons=self._select_buttons, prehear_volume_control=self._prehear_control, crossfader_control=self._crossfader_control, crossfade_buttons=self._crossfade_buttons))
        # self._mixer = MixerComponent(NUM_TRACKS, auto_name=True, is_enabled=False, invert_mute_feedback=True, layer=Layer(volume_controls=self._volume_controls, arm_buttons=self._arm_buttons, solo_buttons=self._solo_buttons, mute_buttons=self._mute_buttons, shift_button=self._shift_button, track_select_buttons=self._select_buttons, prehear_volume_control=self._prehear_control, crossfader_control=self._crossfader_control))
        self._mixer.master_strip().layer = Layer(volume_control=self._master_volume_control, select_button=self._master_select_button)
        self._encoder_mode = ModesComponent(name=u'Encoder_Mode', is_enabled=False)
        self._encoder_mode.default_behaviour = ImmediateBehaviour()
        self._encoder_mode.add_mode(u'pan', [AddLayerMode(self._mixer, Layer(pan_controls=self._mixer_encoders))])
        self._encoder_mode.add_mode(u'sends', [AddLayerMode(self._mixer, Layer(send_controls=self._mixer_encoders)), DelayMode(AddLayerMode(self._mixer, Layer(send_select_buttons=self._send_select_buttons)))])
        self._encoder_mode.add_mode(u'user', [AddLayerMode(self._mixer, Layer(user_controls=self._mixer_encoders))])
        self._encoder_mode.layer = Layer(pan_button=self._pan_button, sends_button=self._sends_button, user_button=self._user_button)
        self._encoder_mode.selected_mode = u'pan'

    def _create_transport(self):
        self._transport = TransportComponent(name='Transport', is_enabled=False, layer=Layer(shift_button=self._shift_button, play_button=self._play_button, stop_button=ComboElement(self._play_button, modifiers=[self._shift_button]), record_button=self._record_button, metronome_button=self._metronome_button, tap_tempo_button=self._tap_tempo_button, nudge_down_button=self._with_shift(self._nudge_down_button), nudge_up_button=self._with_shift(self._nudge_up_button), tempo_encoder=self._tempo_control), play_toggle_model_transform=lambda v: v)
        # self._transport = TransportComponent(name='Transport', is_enabled=False, layer=Layer(shift_button=self._shift_button, play_button=self._play_button, stop_button=ComboElement(self._play_button, modifiers=[self._shift_button]), record_button=self._record_button, metronome_button=self._with_shift(self._tap_tempo_button), tap_tempo_button=self._tap_tempo_button, nudge_down_button=self._with_shift(self._nudge_down_button), nudge_up_button=self._with_shift(self._nudge_up_button), tempo_encoder=self._tempo_control), play_toggle_model_transform=lambda v: v)

    def _create_device(self):
        self._device = DeviceComponent(name=u'Device', is_enabled=False, layer=Layer(parameter_controls=self._device_controls, bank_buttons=self._device_bank_buttons, bank_prev_button=self._device_prev_bank_button, bank_next_button=self._device_next_bank_button, on_off_button=self._device_on_off_button, lock_button=self._device_lock_button), device_selection_follows_track_selection=True)

    def _create_view_control(self):
        self._view_control = DetailViewCntrlComponent(name=u'View_Control', is_enabled=False, layer=Layer(device_nav_left_button=self._prev_device_button, device_nav_right_button=self._next_device_button, device_clip_toggle_button=self._clip_device_button, detail_toggle_button=self._detail_view_button))
        self._view_control.device_clip_toggle_button.pressed_color = u'DefaultButton.On'

    def _create_quantization_selection(self):
        self._quantization_selection = QuantizationComponent(name=u'Quantization_Selection', is_enabled=False, layer=Layer(quantization_buttons=self._quantization_buttons))

    def _create_recording(self):
        record_button = MultiElement(self._session_record_button, self._foot_pedal_button.single_press)
        self._session_recording = SessionRecordingComponent(ClipCreator(), self._view_control, name=u'Session_Recording', is_enabled=False, layer=Layer(new_button=self._foot_pedal_button.double_press, record_button=record_button, _uses_foot_pedal=self._foot_pedal_button))

    def get_matrix_button(self, column, row):
        return self._matrix_rows_raw[row][column]

    def _product_model_id_byte(self):
        return 41

    def _create_background(self):
        self._background = BackgroundComponent(is_root=True)
        self._background.set_enabled(False)
        self._background.layer = Layer(stop_buttons=self._stop_buttons)  # , display_line2=self._display_line2, display_line3=self._display_line3, display_line4=self._display_line4, top_buttons=self._select_buttons, bottom_buttons=self._track_state_buttons, scales_button=self._scale_presets_button, octave_up=self._octave_up_button, octave_down=self._octave_down_button, side_buttons=self._side_buttons, repeat_button=self._repeat_button, accent_button=self._accent_button, double_button=self._double_button, in_button=self._in_button, out_button=self._out_button, param_controls=self._global_param_controls, param_touch=self._global_param_touch_buttons, tempo_control_tap=self._tempo_control_tap, master_control_tap=self._master_volume_control_tap, touch_strip=self._touch_strip_control, touch_strip_tap=self._touch_strip_tap, nav_up_button=self._nav_up_button, nav_down_button=self._nav_down_button, nav_left_button=self._nav_left_button, nav_right_button=self._nav_right_button, aftertouch=self._aftertouch_control, pad_parameters=self._pad_parameter_control, _notification=self._notification.use_single_line(2), priority=consts.BACKGROUND_PRIORITY)

        self._matrix_background = BackgroundComponent()
        self._matrix_background.set_enabled(False)
        self._matrix_background.layer = Layer(matrix=self._session_matrix)

        self._mod_background = ModifierBackgroundComponent(is_root=True)
        # self._mod_background.set_enabled(False)
        self._mod_background.layer = Layer(shift_button=self._shift_button)


    def _create_step_sequencer(self):
        self._matrix_background.set_enabled(False)
        self._step_sequencer = StepSeqComponent(grid_resolution=self._grid_resolution, playhead = self._playhead)
        self._step_sequencer._nav_up_button = self._up_button
        self._step_sequencer._nav_down_button = self._down_button
        self._step_sequencer._nav_left_button = self._left_button
        self._step_sequencer._nav_right_button = self._right_button

        self._step_sequencer.layer = self._create_step_sequencer_layer()
        self._step_sequencer.set_next_loop_page_button = self._right_button
        self._step_sequencer.set_prev_loop_page_button = self._left_button


        # self._drum_velocity_levels = VelocityLevelsComponent(target_note_provider=self._drum_component, skin_base_key=self.drum_group_velocity_levels_skin, is_enabled=False, layer=Layer(velocity_levels=u'velocity_levels_element', select_button=u'select_button'))
        # drum_note_editor = self.note_editor_class(clip_creator=self._clip_creator, grid_resolution=self._grid_resolution, skin_base_key=self.drum_group_note_editor_skin, velocity_provider=self._drum_velocity_levels, velocity_range_thresholds=self.note_editor_velocity_range_thresholds)
        # drum_note_editor = self.note_editor_class(clip_creator=self._clip_creator, grid_resolution=self._grid_resolution)
        # self._note_editor_settings_component.add_editor(drum_note_editor)

        # self._drum_step_sequencer = StepSeqComponent(self._clip_creator, self._skin, name=u'Drum_Step_Sequencer', grid_resolution=self._grid_resolution, instrument_component=self._drum_component, is_enabled=False)


    def _create_step_sequencer_layer(self):

        return Layer(
            velocity_slider=self._velocity_slider,
            drum_matrix=self._session_matrix.submatrix[:4, 1:5],
            # drum_matrix=self._session_matrix.submatrix[:4, 0:5],
            # [4, 1:5],  mess with this for possible future 32 pad drum rack :

            # button_matrix=self._double_press_matrix.submatrix[4:8, 0:4],  # [4:8, 1:5],
            button_matrix=self._double_press_matrix.submatrix[4:8, 1:5],  # [4:8, 1:5],

            #  next_page_button = self._bank_button,

            #select_button=self._user_button,
            delete_button=self._stop_all_button,
            # playhead=self._playhead,
            quantization_buttons=self._stop_buttons,
            shift_button=self._shift_button,
            # loop_selector_matrix=self._double_press_matrix.submatrix[4:8, 4],
            loop_selector_matrix=self._double_press_matrix.submatrix[:8, :1],
            # changed from [:8, :1] so as to enable bottem row of rack   . second value clip length rows
            # short_loop_selector_matrix=self._double_press_event_matrix.submatrix[4:8, 4],
            short_loop_selector_matrix=self._double_press_event_matrix.submatrix[:8, :1],
            # changed from [:8, :1] no change noticed as of yet
            drum_bank_up_button=self._up_button,
            drum_bank_down_button=self._down_button)


    def _create_drum_component(self):
        self._drum_component = DrumGroupComponent(name='Drum_Group', is_enabled=False)
        self._drum_component.layer = Layer(
            drum_matrix=self._session_matrix,
            #    page_strip=self._touch_strip_control,
            #    scroll_strip=self._with_shift(self._touch_strip_control),
            #    solo_button=self._global_solo_button,
            #select_button=self._metronome_button,
            #    delete_button=self._delete_button,
            scroll_page_up_button=self._up_button,
            scroll_page_down_button=self._down_button,
            #    quantize_button=self._quantize_button,
            #    mute_button=self._global_mute_button,
            scroll_up_button=self._with_shift(self._up_button),
            scroll_down_button=self._with_shift(self._down_button))

    # def _create_instrument(self):
    #     instrument_basic_layer = Layer(
    #         # octave_strip=self._with_shift(self._touch_strip_control),
    #         #   capture_button = self._tap_tempo_button,
    #         #scales_toggle_button=self._metronome_button,
    #         octave_up_button=self._up_button,
    #         octave_down_button=self._down_button,
    #         scale_up_button=self._with_shift(self._up_button),
    #         scale_down_button=self._with_shift(self._down_button))

    #     self._instrument = MelodicComponent(skin=self._skin, is_enabled=False,
    #                                         clip_creator=self._clip_creator, name='Melodic_Component',
    #                                         grid_resolution=self._grid_resolution,
    #                                         note_editor_settings=self._add_note_editor_setting(),
    #                                         layer=self._create_instrument_layer(),
    #                                         instrument_play_layer=Layer(
    #                                             octave_up_button=self._up_button,
    #                                             octave_down_button=self._down_button,
    #                                             scale_up_button=self._with_shift(self._up_button),
    #                                             scale_down_button=self._with_shift(self._down_button),
    #                                             matrix=self._session_matrix
    #                                         ),
    #                                         # touch_strip=self._touch_strip_control, touch_strip_indication=self._with_firmware_version(1, 16, ComboElement(self._touch_strip_control, modifiers=[self._select_button])),
    #                                         # touch_strip_toggle=self._with_firmware_version(1, 16, ComboElement(self._touch_strip_tap, modifiers=[self._select_button])),
    #                                         # aftertouch_control=self._aftertouch_control, delete_button=self._delete_button),
    #                                         instrument_sequence_layer=instrument_basic_layer  # + Layer(note_strip=self._touch_strip_control)
    #                                         )
    #     self._on_note_editor_layout_changed.subject = self._instrument



    # def _create_instrument_layer(self):
    #     return Layer(
    #         playhead=self._playhead,
    #         velocity_slider=self._velocity_slider,
    #         # mute_button=self._global_mute_button,
    #         quantization_buttons=self._stop_buttons,
    #         loop_selector_matrix=self._double_press_matrix.submatrix[0:8, 0],  # [:, 0]
    #         short_loop_selector_matrix=self._double_press_event_matrix.submatrix[0:8, 0],  # [:, 0]
    #         #note_editor_matrices=ButtonMatrixElement(
    #         #    [[self._session_matrix.submatrix[:, 4 - row] for row in range(7)]]))
    #         note_editor_matrices=ButtonMatrixElement([[ self._session_matrix.submatrix[:8, 4 - row] for row in range(4)]]))


    # def enter_note_mode_layout(self):
    #     self._matrix_modes.selected_mode = 'user'
    #     self._select_note_mode()

    #     #if self._user_modes.selected_mode == 'instrument':
    #     #    self._instrument._set_selected_mode(self._instrument.selected_mode)
    #     #el
    #     if self._user_modes.selected_mode == 'drums':
    #         self._drum_modes._set_selected_mode(self._drum_modes.selected_mode)

    #     self.reset_controlled_track()

    # def exit_note_mode_layout(self):
    #     self.reset_controlled_track()

    # def switch_note_mode_layout(self):
    #     self._matrix_modes.selected_mode = 'user'
    #     self._select_note_mode()

    #     #if self._user_modes.selected_mode == 'instrument':
    #     #   getattr(self._instrument, 'cycle_mode', nop)()
    #     #el
    #     if self._user_modes.selected_mode == 'drums':
    #         getattr(self._drum_modes, 'cycle_mode', nop)()

    #     self.reset_controlled_track()




    def _create_vu_controls(self):
        # self._sequencer = StepSequencerComponent(self, self._session, self._session_matrix, tuple(self._stop_buttons))
        self._sequencer = StepSequencerComponent(self, self._session, self._session_matrix, tuple(self._double_press_matrix.submatrix[0:8, 0]))
        is_momentary = True
        select_buttons = []
        arm_buttons = []
        solo_buttons = []
        mute_buttons = []
        scene_launch_buttons = [ ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, index + 82) for index in range(NUM_SCENES) ]

        # stop_buttons = [ ConfigurableButtonElement(is_momentary, MIDI_NOTE_TYPE, index, 52) for index in range(NUM_TRACKS) ]
        is_momentary = True
        # self.shift_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 98)
        # self.right_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 96)
        # self.left_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 97)
        # self.up_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 94)
        # self.down_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, 0, 95)


        for track in range(8):
            solo_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 49)
            solo_buttons.append(solo_button)
            mute_button = ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 50)
            mute_buttons.append(mute_button)
            solo_button.name = str(track) + '_Solo_Button'
            mute_button.name = str(track) + '_Mute_Button'
            select_buttons.append(ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 51))
            select_buttons[-1].name = str(track) + '_Select_Button'          
            arm_buttons.append(ButtonElement(is_momentary, MIDI_NOTE_TYPE, track, 48))
            arm_buttons[-1].name = str(track) + '_Arm_Button'

        # self._sequencer.set_bank_buttons(tuple(select_buttons))
        # self._sequencer.set_nav_buttons(self.up_button, self.down_button, self.left_button, self.right_button)
        self._sequencer.set_button_matrix(self._session_matrix)
        # self._sequencer.set_follow_button(self._master_select_button)
        # self._sequencer.set_velocity_buttons(tuple(arm_buttons))
        self._sequencer.set_shift_button(self._shift_button)
        # self._sequencer.set_lane_mute_buttons(tuple(scene_launch_buttons))
        # self._sequencer.set_loop_start_buttons(tuple(mute_buttons))
        # self._sequencer.set_loop_length_buttons(tuple(solo_buttons))

        self.select_buttons = select_buttons
        self.arm_buttons = arm_buttons
        self.mute_buttons = mute_buttons
        self.solo_buttons = solo_buttons

        # self.stop_buttons = stop_buttons

        self.scene_launch_buttons = scene_launch_buttons
        self._scene_launch_buttons.resource_type = PrioritizedResource

        
        def when_bank_on(button):
            return self._bank_toggle.create_toggle_element(on_control=button)

        def when_bank_off(button):
            return self._bank_toggle.create_toggle_element(off_control=button)

        self._vu_session_nav = CustomSessionComponent(NUM_TRACKS, NUM_SCENES, auto_name=True, is_enabled=False,
                                                enable_skinning=True,
                                                layer=Layer(track_bank_left_button=when_bank_off(self._left_button),
                                                            track_bank_right_button=when_bank_off(self._right_button),
                                                            scene_bank_up_button=when_bank_off(self._up_button),
                                                            scene_bank_down_button=when_bank_off(self._down_button),
                                                            page_left_button=when_bank_on(self._left_button),
                                                            page_right_button=when_bank_on(self._right_button),
                                                            page_up_button=when_bank_on(self._up_button),
                                                            page_down_button=when_bank_on(self._down_button)))

    def _create_vu(self):
        def when_bank_on(button):
                    return self._bank_toggle.create_toggle_element(on_control=button)

        def when_bank_off(button):
            return self._bank_toggle.create_toggle_element(off_control=button)
        # self._parent = self 
        # self._parent._button_rows = self._matrix_rows_raw
        # self._parent._track_stop_buttons = self._stop_buttons 
        # self._parent._scene_launch_buttons = self._scene_launch_buttons
        # self._parent._matrix = self._session_matrix
        self._button_rows = self._matrix_rows_raw
        self._matrix_background.set_enabled(False)

        self._vu = VUMeters(self)
        self._vu.layer = Layer(_track_stop_buttons = self._stop_buttons, _scene_launch_buttons = self._scene_launch_buttons, _matrix = self._session_matrix)
        self._vu.disconnect()
        self._vu.disable()

        self._shift_button.add_value_listener(self._shift_value)
        # self._vu._shift_button.add_value_listener(self._vu._shift_value)

    def _shift_value(self,  value):
        if (self._matrix_modes.selected_mode == 'VU' and self._vu != None):
            if value != 0:
                self._vu.disconnect()
                self._vu.disable()
            else:
                self._update_vu_meters()
                self._vu.enable()


    
    def _update_vu_meters(self):
        self._matrix_background.set_enabled(False)

        if self._vu == None and self._matrix_modes.selected_mode == 'VU':
            self._vu = VUMeters(self._parent)
        else:
            self._vu.disconnect()
        self._vu.observe( int(self._session_zoom._session.track_offset()) )

    def _create_matrix_modes(self):

        if self._implicit_arm:
            self._auto_arm = AutoArmComponent(name='Auto_Arm')

        self._matrix_modes = ModesComponent(name='Matrix_Modes', is_root=True)
        self._matrix_modes.default_behaviour = ImmediateBehaviour()
        self._matrix_modes.add_mode('disable', [self._matrix_background, self._background, self._mod_background])
        self._matrix_modes.add_mode('sends', self._session_mode_layers())
        self._matrix_modes.add_mode('session', self._session_mode_layers())
        self._matrix_modes.add_mode('VU', self._vu_mode_layers())
        self._matrix_modes.add_mode('user', self._user_mode_layers())

        self._matrix_modes.layer = Layer(session_button=self._pan_button, sends_button=self._sends_button, user_button=self._user_button, VU_button = self._with_shift(self._bank_button))
        self._on_matrix_mode_changed.subject = self._matrix_modes
        self._matrix_modes.selected_mode = u'session'


    def _session_mode_layers(self):
        self._vu.disconnect()
        self._vu.disable()
        return [self._session, self._view_control, self._session_zoom]#, self._mixer

    def _vu_mode_layers(self):
        
        self._session.set_enabled(False)
        # self._session_zoom._on_zoom_value(1) #zoom out
        self._session_zoom.set_enabled(True)
        self._session_zoom._is_zoomed_out = False
        # self._session_zoom.set_zoom_button(self._parent._shift_button)
        self._session_zoom.update()

        self._update_vu_meters()
        return [self._sequencer, self._view_control, self._session_zoom]



    def _user_mode_layers(self): 
        self._drum_group_finder = DrumGroupFinderComponent()
        self._on_drum_group_changed.subject = self._drum_group_finder
        self._session.set_enabled(False)
        self.reset_controlled_track()

        # self._drum_modes = ModesComponent(name='Drum_Modes', is_enabled=False)
        # self._drum_modes.add_mode('sequencer', self._step_sequencer)
        # #self._drum_modes.add_mode('64pads', self._drum_component)  # added 15:18 subday 22/10/17     can maybe look into this. causes issues when trying to scroll.(drumcomp1)

        # self._drum_modes.selected_mode = 'sequencer'

        #self._user_modes = ModesComponent(name='User_Modes', is_enabled=False)
        #self._user_modes.add_mode('drums', [self._drum_modes])
        #self._user_modes.add_mode('instrument', [self._note_repeat_enabler, self._instrument])
        #self._user_modes.selected_mode = 'drums'

        # return [self._drum_modes, self._view_control, self._matrix_background]  # , self._mixer
        return [self._step_sequencer, self._view_control, self._matrix_background]  # , self._mixer

    # def _user2_mode_layers(self):

    #     self._user_modes = ModesComponent(name='Instrument_Modes', is_enabled=False)
    #     #self._user_modes.add_mode('drums', [self._drum_modes])
    #     self._user_modes.add_mode('instrument', [self._note_repeat_enabler, self._instrument])
    #     self._user_modes.selected_mode = 'instrument'

    #     return [self._user_modes, self._view_control, self._matrix_background]  # , self._mixer

    # def _init_note_repeat(self):
    #     self._note_repeat = NoteRepeatComponent(is_enabled=False,name='Note_Repeat')
    #     self._note_repeat.set_enabled(False)
    #     self._note_repeat.set_note_repeat(self._c_instance.note_repeat)
    #     self._note_repeat.layer = Layer(
    #         # aftertouch_control=self._aftertouch_control,
    #         select_buttons=self._shifted_stop_buttons
    #         # pad_parameters=self._pad_parameter_control
    #     )
    #     self._note_repeat.layer.priority = consts.DIALOG_PRIORITY
    #     self._note_repeat_enabler = EnablingModesComponent(name='Note_Repeat_Enabler', component=self._note_repeat,
    #                                                        toggle_value='DefaultButton.Alert',
    #                                                        disabled_value='DefaultButton.On')
    #     self._note_repeat_enabler.set_enabled(False)
    #     self._note_repeat_enabler.layer = Layer(toggle_button=self._with_shift(self._bank_button))




    # def _select_note_mode(self):
    #     """
    #     Selects which note mode to use depending on the kind of
    #     current selected track and its device chain...
    #     """
    #     track = self.song().view.selected_track
    #     drum_device = self._drum_group_finder.drum_group
    #     self._step_sequencer.set_drum_group_device(drum_device)
    #     self._drum_component.set_drum_group_device(drum_device)
    #     if track == None or track.is_foldable or track in self.song().return_tracks or track == self.song().master_track or track.is_frozen:
    #         self._user_modes.selected_mode = 'disabled'
    #     elif track and track.has_audio_input:
    #         self._user_modes.selected_mode = 'disabled'
    #         #self._note_modes.selected_mode = 'looper'
    #     elif drum_device:
    #         self._user_modes.selected_mode = 'drums'
    #     #else:
        #    self._user_modes.selected_mode = 'instrument'
        #self.reset_controlled_track()


    @subject_slot('value')
    def value_changed(self, value):
        print('value_changed')
        print(value)
        '''if self.is_enabled() and not self._device_mode:
            if value > 0 or not self._bank_down_button.is_momentary():
                new_mode = max(self._mode_index - 1, 0)
                self.set_mode(new_mode)'''


    @subject_slot('drum_group')
    def _on_drum_group_changed(self):
        #self._shift_button.receive_value(127)
        # #self.schedule_message(1, self.resetshift)
        self._matrix_background.set_enabled(True)
        # self.schedule_message(1, self.disablebackground)
        self.reset_controlled_track()
        self._matrix_background.set_enabled(False)

        # if self._matrix_modes.selected_mode != 'session':
        #     pass
            #self._select_note_mode()

    def resetshift(self):
            self._shift_button.receive_value(0)

    def shiftmodedisable(self):
        self._matrix_modes.selected_mode = 'disabled'

    def disablebackground(self):
        self._matrix_background.set_enabled(False)



    @subject_slot('selected_mode')
    def _on_matrix_mode_changed(self, mode):
        #self._shift_button.receive_value(127)
        #self.schedule_message(1, self.resetshift)
        self._vu.disconnect()
        self._vu.disable() 

        self._matrix_background.set_enabled(True)
        self.schedule_message(1, self.disablebackground)
        self.reset_controlled_track()
        self._update_auto_arm(selected_mode=mode)

        # if self._matrix_modes.selected_mode != 'disabled':
        #     if self._implicit_arm:
        #         self._update_auto_arm(selected_mode=mode)
        #     self.reset_controlled_track()


        self.reset_controlled_track()

        if self._matrix_modes.selected_mode == 'VU':
            self._matrix_background.set_enabled(False)


    def _update_auto_arm(self, selected_mode=None):
        self._auto_arm.set_enabled(selected_mode or self._matrix_modes.selected_mode == 'user')

    # @subject_slot('selected_mode')
    # def _on_note_editor_layout_changed(self, mode):
    #     self.reset_controlled_track()
    #     # pass
    #    # self.reset_controlled_track(mode)


    def reset_controlled_track(self, mode=None):
        #if mode == None:
        #   mode = self._instrument.selected_mode
        #if self._instrument and self._instrument.is_enabled() and mode == 'sequence':
        #    self.release_controlled_track()
        #else:
        self.set_controlled_track(self.song().view.selected_track)



    def _add_note_editor_setting(self):
        return NoteEditorSettingsComponent(self._grid_resolution,
                                           Layer(initial_encoders=self._mixer_encoders),
                                           Layer(encoders=self._mixer_encoders))



    def _on_track_offset_changed(self):
        self._matrix_modes._on_track_offset_changed()
        if self._matrix_modes == 'VU':
            self._update_vu_meters()



    def get_matrix_button(self, column, row):
        return self._matrix_rows_raw[row][column]

    def _product_model_id_byte(self):
        return 41

    # def disconnect(self):
    #     self._matrix_modes.selected_mode = 'disabled'
    #     self._background.set_enabled(False)
    #     control_surface.disconnect(self)
        # return None


    @contextmanager
    def component_guard(self):
        """ Customized to inject additional things """
        with super(APC40_CJedit, self).component_guard():

            with self.make_injector().everywhere():
                yield

    def make_injector(self):
        """ Adds some additional stuff to the injector, used in BaseMessenger """
        return inject(
            double_press_context=const(self._double_press_context),
            control_surface=const(self),
            log_message=const(self.log_message))
