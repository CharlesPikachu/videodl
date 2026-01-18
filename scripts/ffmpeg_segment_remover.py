'''
Function:
    Implementation of FFmpegSegmentRemover
Author:
    Zhenchao Jin
WeChat Official Account (微信公众号):
    Charles的皮卡丘
'''
from pathlib import Path
import argparse, json, shutil, subprocess, tempfile


'''FFmpegSegmentRemover'''
class FFmpegSegmentRemover:
    def __init__(self, ffmpeg="ffmpeg", ffprobe="ffprobe", overwrite=False, dry_run=False):
        self.ffmpeg, self.ffprobe = ffmpeg, ffprobe
        self.overwrite, self.dry_run = overwrite, dry_run
    '''runcmd'''
    def runcmd(self, cmd):
        if self.dry_run: print("CMD:", " ".join(cmd)); return ""
        p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        if p.returncode != 0: raise RuntimeError(f"Command failed:\n{' '.join(cmd)}\n\n{p.stdout}")
        return p.stdout
    '''checkbins'''
    def checkbins(self):
        self.runcmd([self.ffmpeg, "-version"])
        self.runcmd([self.ffprobe, "-version"])
    '''duration'''
    def duration(self, inp):
        out = self.runcmd([self.ffprobe, "-v", "error", "-show_entries", "format=duration", "-of", "json", inp])
        return float(json.loads(out)["format"]["duration"]) if out else 0.0
    '''parsetime'''
    @staticmethod
    def parsetime(s: str) -> float:
        s = s.strip()
        if ":" not in s: return float(s)
        parts = s.split(":")
        parts = [float(p) for p in parts]
        if len(parts) == 2: m, sec = parts; return m * 60 + sec
        if len(parts) == 3: h, m, sec = parts; return h * 3600 + m * 60 + sec
        raise ValueError(f"Invalid time format: {s}")
    '''normalizeranges'''
    @staticmethod
    def normalizeranges(ranges, dur):
        rr = []
        for a, b in ranges:
            a, b = float(a), float(b)
            if b < a: a, b = b, a
            a, b = max(0.0, min(dur, a)), max(0.0, min(dur, b))
            if b > a: rr.append((a, b))
        rr.sort(); merged = []
        for a, b in rr:
            if not merged or a > merged[-1][1]: merged.append([a, b])
            else: merged[-1][1] = max(merged[-1][1], b)
        return [tuple(x) for x in merged]
    '''invertranges'''
    @staticmethod
    def invertranges(remove_ranges, dur):
        keep, cur = [], 0.0
        for a, b in remove_ranges:
            if a > cur: keep.append((cur, a))
            cur = max(cur, b)
        if cur < dur: keep.append((cur, dur))
        return keep
    '''remove'''
    def remove(self, inp, outp, remove_ranges):
        inp_p, out_p = Path(inp), Path(outp)
        if not inp_p.exists(): raise FileNotFoundError(f"Input not found: {inp}")
        if out_p.exists() and not self.overwrite: raise FileExistsError(f"Output exists (use --overwrite): {outp}")
        self.checkbins()
        dur = self.duration(str(inp_p))
        rm = self.normalizeranges(remove_ranges, dur)
        keep = self.invertranges(rm, dur)
        if not keep: raise RuntimeError("Remove ranges cover the whole video; nothing to output.")
        tmpdir = Path(tempfile.mkdtemp(prefix="ffcut_"))
        try:
            segs = []
            for i, (a, b) in enumerate(keep):
                seg = tmpdir / f"keep_{i:03d}.mkv"
                t = max(0.0, b - a)
                self.runcmd([self.ffmpeg, "-y" if self.overwrite else "-n", "-i", str(inp_p), "-ss", f"{a:.6f}", "-t", f"{t:.6f}", "-map", "0", "-c", "copy", "-avoid_negative_ts", "make_zero", "-reset_timestamps", "1", str(seg)])
                segs.append(seg)
            if not segs: raise RuntimeError("No kept segments were produced.")
            concat_txt = tmpdir / "concat.txt"
            concat_txt.write_text("".join([f"file '{p.as_posix()}'\n" for p in segs]), encoding="utf-8")
            merged = tmpdir / "merged.mkv"
            self.runcmd([self.ffmpeg, "-y" if self.overwrite else "-n", "-f", "concat", "-safe", "0", "-i", str(concat_txt), "-c", "copy", str(merged)])
            self.runcmd([self.ffmpeg, "-y" if self.overwrite else "-n", "-i", str(merged), "-i", str(inp_p), "-map", "0", "-map_metadata", "1", "-map_chapters", "1", "-c", "copy", str(out_p)])
        finally:
            if self.dry_run: print(f"Temp dir kept (dry-run): {tmpdir}")
            else: shutil.rmtree(tmpdir, ignore_errors=True)


'''buildcmdparser'''
def buildcmdparser():
    parser = argparse.ArgumentParser(description="Remove specified time ranges from a video with ffmpeg stream-copy (-c copy). Times can be seconds (12.3) or hh:mm:ss[.ms]. Supports multiple --remove START END pairs.")
    parser.add_argument("input", help="Input video path")
    parser.add_argument("output", help="Output video path")
    parser.add_argument("-r", "--remove", nargs=2, action="append", required=True, metavar=("START", "END"), help='Time range to remove. Example: "-r 12.3 45.7" or "-r 00:01:12.3 00:01:45.7". You can repeat -r multiple times.')
    parser.add_argument("--ffmpeg", default="ffmpeg", help="Path/name of ffmpeg (default: ffmpeg)")
    parser.add_argument("--ffprobe", default="ffprobe", help="Path/name of ffprobe (default: ffprobe)")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite output if it exists")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing")
    return parser


'''main'''
def main():
    args = buildcmdparser().parse_args()
    remover = FFmpegSegmentRemover(args.ffmpeg, args.ffprobe, overwrite=args.overwrite, dry_run=args.dry_run)
    ranges = [(remover.parsetime(a), remover.parsetime(b)) for a, b in args.remove]
    remover.remove(args.input, args.output, ranges)
    if not args.dry_run: print("Done:", args.output)


'''tests'''
if __name__ == "__main__":
    main()