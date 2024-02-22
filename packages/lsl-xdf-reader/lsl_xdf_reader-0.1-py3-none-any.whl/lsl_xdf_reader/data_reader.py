import traceback
import pyxdf as xd
import csv
import os
import glob
import sys
from datetime import datetime
import tkinter as tk
from tkinter.filedialog import askdirectory

tk.Tk().withdraw()

timeObj = datetime.now()
timestr = timeObj.strftime("%Y%m%d-%H%M%S")


def write_error(error, stream_name, error_messages):
    error_message = "----------------------------------------------------------------------\n"
    error_message += f"An error occurred in stream: {stream_name}\n"
    error_message += "".join(traceback.format_exception(*error)) + "\n"
    error_messages.append(error_message)


def create_headers(Time_Series, stream, stream_name, error_messages):
    Headers = ["LSL Timestamp"]
    try:
        if 'info' in stream and 'desc' in stream['info'] and len(stream['info']['desc']) > 0 and \
           'channels' in stream['info']['desc'][0] and len(stream['info']['desc'][0]['channels']) > 0 and \
           'channel' in stream['info']['desc'][0]['channels'][0] and len(stream['info']['desc'][0]['channels'][0]['channel']) > 0:
            for x in stream['info']['desc'][0]['channels'][0]['channel']:
                header = [x['label'][0] or "None", x['unit'][0].replace("ÂºC", "Degrees C").replace("μM", "uM") or "None"]
                Headers.append(header[0] + '(' + header[1] + ')')
        else:
            Headers += [str(x + 1) for x in range(len(Time_Series[0]))]
    except:
        Headers += [str(x + 1) for x in range(len(Time_Series[0]))]
        write_error(sys.exc_info(), stream_name, error_messages)

    return [h.replace(' ', '_') for h in Headers]


def write_all_exp(st, stream, file, indir, success_messages, error_messages):
    if (stream['footer']['info']['sample_count'][0]) != '0':
        Time_Stamps = stream['time_stamps']
        Time_Series = stream['time_series']
        Headers = create_headers(Time_Series, stream, st, error_messages)

        file = os.path.splitext(file)[0]
        file = os.path.basename(file)
        outdir = os.path.join(indir, file + "_" + timestr + "_OutputFiles")
        os.makedirs(outdir, exist_ok=True)

        sRate = float(stream['footer']['info']['sample_count'][0]) / (
                float(stream['footer']['info']['last_timestamp'][0]) -
                float(stream['footer']['info']['first_timestamp'][0]))

        with open(os.path.join(outdir, st + '_allExp.csv'), 'w', newline='\n') as csvfile:
            wrt = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            wrt.writerow(Headers)
            for i, datum in enumerate(Time_Series):
                wrt.writerow([Time_Stamps[i]] + list(datum))

        with open(os.path.join(outdir, st + '_allExp_Report.csv'), 'w', newline='\n') as csvfile:
            wrt = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            wrt.writerow(["Name:", stream['info']['name'][0]])
            wrt.writerow(["Hostname:", stream['info']['hostname'][0]])
            wrt.writerow(["Creation:", stream['info']['created_at'][0]])
            wrt.writerow(["Data Type:", stream['info']['channel_format'][0]])
            wrt.writerow(["Channel Count:", stream['info']['channel_count'][0]])
            wrt.writerow(["Sample Count:", stream['footer']['info']['sample_count'][0]])
            wrt.writerow(["Nominal Sampling Rate:", stream['info']['nominal_srate'][0]])
            wrt.writerow(["Effective Sampling Rate:", str(sRate)])
            wrt.writerow(["First Adjusted Timestamp:", str(stream['time_stamps'][0])])
            wrt.writerow(["Last Adjusted Timestamp:", str(stream['time_stamps'][-1])])
            wrt.writerow(["Adjusted Timestamp Space:", str(stream['time_stamps'][-1] - stream['time_stamps'][0])])
            wrt.writerow(["First Non-Adjusted Timestamp:", stream['footer']['info']['first_timestamp'][0]])
            wrt.writerow(["Last Non-Adjusted Timestamp:", stream['footer']['info']['last_timestamp'][0]])
            wrt.writerow(["Non-Adjusted Timestamp Space:",
                          str(float(stream['footer']['info']['last_timestamp'][0]) - float(
                              stream['footer']['info']['first_timestamp'][0]))])

        success_messages.append(st + "AllExp DONE!")
        return 1
    else:
        write_error(sys.exc_info(), st, error_messages)
        return sys.exc_info()[0]


def parse_xdf(fdir):
    streams = {}
    indir = fdir + "/"
    success_messages = []
    error_messages = []
    for file in glob.glob(os.path.join(indir, "*.xdf")):
        data = xd.load_xdf(file)
        for st in data[0]:
            streams[st['info']['name'][0] + " - " + st['info']['type'][0].replace(":", "")] = st

        for st in streams.keys():
            write_all_exp(st, streams[st], file, indir, success_messages, error_messages)

    print("\n".join(success_messages), end="\n\n")
    print("\n".join(error_messages))


def main():
    directory = askdirectory()
    parse_xdf(directory)


if __name__ == "__main__":
    sys.exit(main())
