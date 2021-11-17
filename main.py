import os
import shutil
import pretty_midi
import soundfile
import pyrubberband as pyrb


def pitch_shift(orgdata_path, augdata_path, song_name, n=2):
    audio_data, sample_rate = soundfile.read(os.path.join(orgdata_path, 'wav', song_name+'.wav'))
    midi_data = pretty_midi.PrettyMIDI(os.path.join(orgdata_path, 'mid', song_name+'.mid'))

    for semitone in range(-n, n + 1):
        if semitone == 0:
            continue
        elif semitone < 0:
            wav_file = song_name + '_ps' + f'{semitone}' + '.wav'
            midi_file = song_name + '_ps' + f'{semitone}' + '.mid'
            txt_file = song_name + '_ps' + f'{semitone}' + '.txt'
        else:
            wav_file = song_name + '_ps+' + f'{semitone}' + '.wav'
            midi_file = song_name + '_ps+' + f'{semitone}' + '.mid'
            txt_file = song_name + '_ps+' + f'{semitone}' + '.txt'

        shifted_audio = pyrb.pitch_shift(audio_data, sample_rate, semitone)
        soundfile.write(os.path.join(augdata_path, 'wav', wav_file), shifted_audio, sample_rate)

        shifted_midi = pretty_midi.PrettyMIDI()
        for inst in midi_data.instruments:
            new_inst = pretty_midi.Instrument(program=inst.program)
            for note in inst.notes:
                new_note = pretty_midi.Note(velocity=note.velocity, pitch=note.pitch + semitone, start=note.start,
                                            end=note.end)
                new_inst.notes.append(new_note)
            shifted_midi.instruments.append(new_inst)
        shifted_midi.write(os.path.join(augdata_path, 'mid', midi_file))

        shutil.copy(os.path.join(orgdata_path, 'txt', song_name+'.txt'), os.path.join(augdata_path, 'txt', txt_file))


def time_stretch(orgdata_path, augdata_path, song_name, n=4):
    audio_data, sample_rate = soundfile.read(os.path.join(orgdata_path, 'wav', song_name + '.wav'))
    midi_data = pretty_midi.PrettyMIDI(os.path.join(orgdata_path, 'mid', song_name + '.mid'))

    for rate in [1 + i / 10 for i in range(-n, n + 1)]:
        if int(100 * rate) == 100:
            continue
        else:
            wav_file = song_name + '_ts' + f'{int(100 * rate)}' + '.wav'
            midi_file = song_name + '_ts' + f'{int(100 * rate)}' + '.mid'
            txt_file = song_name + '_ts' + f'{int(100 * rate)}' + '.txt'

        stretched_audio = pyrb.time_stretch(audio_data, sample_rate, rate)
        soundfile.write(os.path.join(augdata_path, 'wav', wav_file), stretched_audio, sample_rate)

        stretched_midi = pretty_midi.PrettyMIDI()
        for inst in midi_data.instruments:
            new_inst = pretty_midi.Instrument(program=inst.program)
            for note in inst.notes:
                new_note = pretty_midi.Note(velocity=note.velocity, pitch=note.pitch, start=note.start * rate,
                                            end=note.end * rate)
                new_inst.notes.append(new_note)
            stretched_midi.instruments.append(new_inst)
        stretched_midi.write(os.path.join(augdata_path, 'mid', midi_file))

        shutil.copy(os.path.join(orgdata_path, 'txt', song_name + '.txt'), os.path.join(augdata_path, 'txt', txt_file))

def create_directory(base_directory):
    dir_list = ['mid', 'txt', 'wav']
    for dir_name in dir_list:
        if not os.path.exists(os.path.join(base_directory, dir_name)):
            os.makedirs(os.path.join(base_directory, dir_name))


if __name__ == '__main__':
    orgdata_path = os.path.join(os.getcwd(), 'original_dataset')
    augdata_path_ps = os.path.join(os.getcwd(), 'aug_dataset', 'pitch_shift')
    augdata_path_ts = os.path.join(os.getcwd(), 'aug_dataset', 'time_stretch')

    create_directory(orgdata_path)
    create_directory(augdata_path_ps)
    create_directory(augdata_path_ts)

    txt_list = os.listdir(os.path.join(orgdata_path, 'txt'))
    midi_list = os.listdir(os.path.join(orgdata_path, 'mid'))
    for i in range(len(txt_list)):
        pitch_shift(orgdata_path, augdata_path_ps, txt_list[i][:len(txt_list[i])-4], n=2)
        time_stretch(orgdata_path, augdata_path_ts, txt_list[i][:len(txt_list[i])-4], n=4)
