# -*- coding: utf-8 -*-
"""Build the six task programs, record real console sessions, render screenshots."""
import io, json, os, subprocess

BASE = r'D:\learning\C语言程序设计\实验4'
WORK = os.path.join(BASE, '_work')
SRC_UTF8 = os.path.join(WORK, 'src')
SHOTS = os.path.join(WORK, 'shots')
GCC = r'C:\msys64\ucrt64\bin\gcc.exe'
os.environ['PATH'] = r'C:\msys64\ucrt64\bin;' + os.environ['PATH']
PROMPT = r'D:\learning\C语言程序设计\实验4>'
os.makedirs(SHOTS, exist_ok=True)

TASKS = [1, 2, 3, 4, 5, 6]
SOURCE = {1: 'task1.c', 2: 'task2.c', 3: 'task3.c', 4: 'task4.c',
          5: 'exp4-1.c', 6: 'exp4-2.c'}
EXE = {n: ('task%d.exe' % n if n <= 4 else 'exp4-%d.exe' % (n - 4)) for n in TASKS}

# prompts of each program, in the order they appear
PROMPTS = {
    1: ['请输入一卡通充值金额（元）：'],
    2: ['请输入一卡通余额（元）：', '请输入本次消费金额（元）：'],
    3: ['请输入三个实数：'],
    4: ['请输入水果重量（kg）与单价（元）：'],
    5: ['请输入菜单选项（1/2/3）：'],
    6: ['请输入菜单选项（1/2/3）：', '请输入充值金额：', '请输入消费金额：'],
}

# each run: (stdin tokens, lines typed at the prompts)
RUNS = {
    1: [(['1200'], ['1200']), (['800'], ['800'])],
    2: [(['1000', '300'], ['1000', '300']), (['500', '800'], ['500', '800'])],
    3: [(['3.5', '7.2', '4.8'], ['3.5  7.2  4.8'])],
    4: [(['3', '6'], ['3  6']), (['6', '5'], ['6  5'])],
    5: [(['2'], ['2'])],
    6: [(['1'], ['1']), (['3', '1200'], ['3', '1200']), (['2', '300'], ['2', '300'])],
}

log = []


def emit(s):
    log.append(s)
    print(s)


# 1) write the four new sources as GBK + CRLF
for n in (1, 2, 3, 4):
    text = io.open(os.path.join(SRC_UTF8, 'task%d.c' % n), encoding='utf-8').read()
    text = text.replace('\r\n', '\n').replace('\n', '\r\n')
    with open(os.path.join(BASE, 'task%d.c' % n), 'wb') as f:
        f.write(text.encode('gbk'))
    emit('wrote task%d.c (GBK, CRLF)' % n)

# 2) strict check compile (warnings must be empty)
for n in TASKS:
    p = subprocess.run([GCC, '-std=c99', '-Wall', '-Wextra', '-O2', '-fsyntax-only',
                        SOURCE[n]], cwd=BASE, capture_output=True)
    emit('check %s rc=%d %s' % (SOURCE[n], p.returncode,
                                (p.stdout + p.stderr).decode('gbk', 'replace').strip()))

# 3) real build, exactly the command shown in the screenshot
for n in TASKS:
    cmd = [GCC, '-o', EXE[n], SOURCE[n]]
    p = subprocess.run(cmd, cwd=BASE, capture_output=True)
    emit('build %s rc=%d %s' % (' '.join(cmd[1:]), p.returncode,
                                (p.stdout + p.stderr).decode('gbk', 'replace').strip()))

# 4) run & capture, and assemble the console transcript
sessions = {}
for n in TASKS:
    exe = os.path.join(BASE, EXE[n])
    runs = []
    for stdin_tokens, typed in RUNS[n]:
        data = (' '.join(stdin_tokens) + '\n').encode('gbk')
        p = subprocess.run([exe], input=data, capture_output=True, cwd=BASE)
        raw = p.stdout.decode('gbk', 'replace').replace('\r\n', '\n')
        # rebuild the terminal view: prompt, typed line, then the program output
        text = raw
        segments = []
        pos = 0
        for line in typed:
            hits = [text.find(pr, pos) for pr in PROMPTS[n]]
            hits = [h for h in hits if h >= 0]
            if not hits:
                raise SystemExit('no prompt left for %r in task %d' % (line, n))
            k = min(hits)
            pr = [p for p in PROMPTS[n] if text.find(p, pos) == k][0]
            k += len(pr)
            segments.append(text[pos:k])
            segments.append(line + '\n')
            pos = k
        segments.append(text[pos:])
        transcript = ''.join(segments)
        runs.append({'stdout': raw, 'transcript': transcript, 'rc': p.returncode,
                     'stderr': p.stderr.decode('gbk', 'replace')})
    sessions[n] = runs

# 5) build the display text of each screenshot
displays = {}
for n in TASKS:
    lines = [PROMPT + 'gcc -o %s %s' % (EXE[n], SOURCE[n]), '']
    for r in sessions[n]:
        lines.append(PROMPT + EXE[n])
        lines.extend(r['transcript'].split('\n'))
        if lines[-1] == '':
            lines.pop()
        lines.append('')
    while lines and lines[-1] == '':
        lines.pop()
    displays[n] = lines

io.open(os.path.join(WORK, 'sessions.json'), 'w', encoding='utf-8').write(
    json.dumps({'displays': displays, 'raw': sessions}, ensure_ascii=False, indent=1))
io.open(os.path.join(WORK, 'build.log'), 'w', encoding='utf-8').write('\n'.join(log))
for n in TASKS:
    emit('--- task %d ---' % n)
    emit('\n'.join(displays[n]))
print('DONE')
