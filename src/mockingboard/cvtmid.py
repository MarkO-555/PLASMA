import sys
#from mido import MidiFile
import mido

optarg     = 1
timescale  = 16.0 # Scale time to 16th of a second
extperchan = 9    # Default to standard MIDI channel  10 for extra percussion
channels = []
if len(sys.argv) == 1:
    print('Usage:', sys.argv[0], '[-p extra_percussion_channel] [-t timescale] MIDI_file')
    sys.exit(0)
# Parse optional arguments
while optarg < (len(sys.argv) - 1):
    if sys.argv[optarg] == '-t': # Override tempo percentage
        timescale = float(sys.argv[optarg + 1]) * 16.0
        optarg += 1 #2
    elif sys.argv[optarg] == '-p': # Add extra percussion channel
        extperchan = int(sys.argv[optarg + 1])
        channels.append(extperchan)
        optarg += 1 #2
    elif sys.argv[optarg][0] == '+': # Enable channel
        channels.append(int(sys.argv[optarg][1]))
        #optarg += 1
    optarg += 1
mid = mido.MidiFile(sys.argv[optarg])
timeshift = timescale
#totaltime = 0.0
eventtime = 0.0
for msg in mid:
    eventtime += msg.time * timeshift
    #totaltime += eventtime
    deltatime = int(round(eventtime))
    #print '; time = ', msg.time
    if msg.type == 'note_on' or msg.type == 'note_off':
        #if eventtime > 0.0 and eventtime < 0.5:
        #    eventtime = 0.5
        octave    = int(msg.note / 12 - 1)
        onote     = int(msg.note % 12)
        lrchan    = int(msg.channel & 1)
        vol       = int(msg.velocity >> 3)
        if msg.velocity > 0 and vol == 0:
            vol = 1
        if msg.type == 'note_off':
            vol = 0
        if octave < 0:
            octave = 0
        if msg.channel in channels:
            if msg.channel == 9 or msg.channel == extperchan:
                #
                # Percussion
                #
                if vol > 0:
                    print('\t!BYTE\t${0:02X}, ${1:02X}, ${2:02X}\t; Percussion {3:d} Chan {4:d} Dur {5:d}'.format(deltatime, msg.note ^ 0x40, (lrchan << 7) | vol, msg.note, msg.channel, vol))
                    if extperchan == 9: # Play percussion on both channels if no extended percussion
                        print('\t!BYTE\t${0:02X}, ${1:02X}, ${2:02X}\t; Percussion {3:d} Chan {4:d} Dur {5:d}'.format(0, msg.note ^ 0x40, vol, msg.note, msg.channel, vol))
                    eventtime = 0.0
            else:
                #
                # Note
                #
                print('\t!BYTE\t${0:02X}, ${1:02X}, ${2:02X}\t; Note {3:d} Chan {4:d} Vol {5:d}'.format(deltatime, 0x80 | (octave << 4) | onote, (lrchan << 7) | vol, msg.note, msg.channel, vol))
                eventtime = 0.0
    elif msg.type == 'set_tempo':
        pass
        #timeshift = msg.tempo / 500000.0 * timescale
        #print '; timescale = ', timescale
    elif msg.type == 'time_signature':
        pass
    elif msg.type == 'control_chage':
        print('; Control change Chan {0:d}'.format(msg.channel))
    elif msg.type == 'program_change':
        print('; Program change Chan {0:d}'.format(msg.channel))
print('\t!BYTE\t${0:02X}, $00, $00'.format(int(eventtime + 0.5)))
