# -*- coding: utf-8 -*-
"""Fill the lab report template with analysis, code and screenshots."""
import io, os, shutil
import docx
from PIL import Image
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Pt, Mm, Emu

BASE = r'D:\learning\C语言程序设计\实验4'
WORK = os.path.join(BASE, '_work')
SHOTS = os.path.join(WORK, 'shots')
DOC_IN = os.path.join(BASE, '实验四-20260305030X-xxx.docx')
DOC_OUT = os.path.join(BASE, '实验四-20260305030X-xxx.docx')
BACKUP = os.path.join(WORK, 'backup_模板.docx')

CN = '宋体'
CODE_FONT = 'Consolas'
BODY_PT = 12          # 小四
BODY_LINE = 21        # 固定值21磅
CODE_PT = 9
CODE_LINE = 12.5

# ---------------------------------------------------------------- content ---
SRC = {1: 'task1.c', 2: 'task2.c', 3: 'task3.c', 4: 'task4.c',
       5: 'exp4-1.c', 6: 'exp4-2.c'}

TASK = {
1: [
 '① 本任务只有“充值金额是否达到1000元”两种情况，属于典型的双分支问题，用 if…else 语句实现即可，不必使用 switch。',
 '② 充值金额可能带小数，用 float 型变量 amount 存放；积分是整数，用 int 型变量 point 存放。',
 '③ 用 scanf("%f",&amount) 读入金额；当 amount>=1000 时，按“每满100元得1积分”计算 point=(int)(amount/100.0f)，其中强制类型转换 (int) 完成取整；金额不足1000时 point=0。',
 '④ 用 printf 输出“本次充值可奖励xx积分”，并对未达到奖励条件的情况给出提示，使程序对两种情况都有反馈。',
],
2: [
 '① 本任务判断“消费金额是否不超过余额”，结果只有刷卡成功和余额不足两种，是典型的二选一问题，用 if…else 实现。',
 '② 余额和消费金额都可能带小数，分别定义为 float 型变量 balance、cost。',
 '③ 依次读入余额和消费金额；当 cost<=balance 时刷卡成功，执行 balance=balance-cost 更新余额并输出消费金额与剩余余额；否则输出“余额不足，请充值”，余额保持不变。',
 '④ 条件写成 <= 而不是 <，可以保证“消费金额刚好等于余额”时也能刷卡成功，符合题目“小于等于”的要求。',
],
3: [
 '① 三个数中求最大值需要两两比较，单靠一个 if 无法完成，采用 if 语句的嵌套实现。',
 '② 三个实数和最大值都用 float 型变量 a、b、c、max 存放，用 scanf("%f%f%f",&a,&b,&c) 一次读入三个数。',
 '③ 先比较 a 与 b：若 a>=b，则 a 是两者中较大的一个，再与 c 比较，a>=c 时 max=a，否则 max=c；若 a<b，则 b 是较大的一个，再与 c 比较，b>=c 时 max=b，否则 max=c。',
 '④ 比较时使用 >= 而不是 >，两数相等时结果同样正确；最后用 printf 按 %.2f 输出最大值。',
],
4: [
 '① 消费金额随重量分三段计价，属于多分支问题，用 if…else if…else 语句实现。',
 '② 重量、单价和应付金额都可能带小数，分别定义为 float 型变量 weight、price、total。',
 '③ 读入重量和单价后按区间判断：weight<2 时 total=weight*price；2<=weight<5 时 total=weight*price*0.9；weight>=5 时 total=weight*price*0.8。',
 '④ 因为 else if 只在前一个条件不成立时才继续判断，所以第二个分支只写 weight<5 就等价于“2<=weight<5”，不必重复写下界；最后用 %.2f 输出金额。',
],
5: [
 '① 菜单只有 1、2、3 三个固定的等值分支，每个取值对应一段处理，用 switch…case 结构比多分支 if 更清晰，也便于以后增加菜单项。',
 '② 定义 int 型变量 menu 保存菜单选项，先输出菜单说明，再用 scanf("%d",&menu) 读入用户的选择。',
 '③ switch(menu) 中 case 1、case 2、case 3 分别输出查询余额、消费、充值的欢迎信息，每个 case 末尾用 break 跳出，避免“贯穿”执行下一个分支。',
 '④ 其他取值由 default 处理，提示“输入的菜单选项有误，请输入1、2或3！”，使程序对非法输入也有响应。',
],
6: [
 '① 在任务5的 switch 菜单框架上增加具体业务：case 1 查询余额，case 2 消费，case 3 充值。',
 '② 定义 float 型变量 balance（初值1000.0）、cost、amount，以及 int 型变量 bonus 保存本次奖励积分。',
 '③ 查询：直接输出 balance。消费：读入 cost，若 cost<=balance 则执行 balance-=cost 并输出消费成功与新余额，否则提示余额不足、余额不变。充值：读入 amount 后先执行 balance+=amount，再按“充值到账后的累计余额”判断积分。',
 '④ 积分判断为多分支：amount>=1000 且 balance>=2000 奖励100积分；否则 (amount>=500 且 balance>=1000) 或 amount>=800 奖励50积分；否则 amount>=200 奖励20积分；其余不奖励。条件中同时出现 && 和 ||，用括号明确运算顺序（&& 优先级高于 ||）。',
],
}

SUMMARY = {
'1.实验结果分析：': [
 '（1）六个程序均在 Dev-C++（gcc）下编译通过，无错误、无警告，运行结果与题目要求一致：任务1输入1200元输出“本次充值可奖励12积分”；任务2输入余额1000元、消费300元输出“刷卡成功”并显示余额700.00元，输入余额500元、消费800元输出“余额不足，请充值”；任务3输入3.5、7.2、4.8输出最大值7.20；任务4输入3kg、6元/kg输出16.20元（九折），输入6kg、5元/kg输出24.00元（八折）；任务5输入菜单2输出“欢迎进入一卡通消费功能”；任务6分别查询余额、充值1200元、消费300元，余额（1000.00→2200.00→700.00）与积分（100积分）均正确。',
 '（2）由运行结果可以看出，if…else 适合处理范围判断和不等式比较，switch…case 适合处理等值判断；六个任务覆盖了关系运算、逻辑运算、条件运算以及两种选择结构的嵌套使用。对1000、2kg、5kg、消费金额等于余额等边界值的测试均通过，说明条件表达式的写法是正确的。',
],
'2.问题：': [
 '（1）任务3最初把格式串写成 scanf("%f,%f,%f",…)，输入时却用空格分隔，格式串与实际输入不匹配，导致 b、c 没有被正确读入，输出的最大值是错的。',
 '（2）任务5最初在 case 1 后面漏写 break，输入1时三个分支的欢迎信息被连续打印出来，出现“贯穿”现象。',
 '（3）任务6中积分条件最初写成 amount>=500 && balance>=1000 || amount>=800，没有加括号，&& 与 || 的先后顺序容易看错；另外最初先判断积分再累加余额，“余额累计”用的是充值前的余额，积分档次算错。',
 '（4）任务1最初把积分写成 (int)amount/100，先取整再除以100，结果恒为0，与“每满100元得1积分”的题意不符。',
],
'3.解决方法及心得：': [
 '（1）scanf 的格式串要与实际输入形式一致，普通数据用空格分隔即可；读入后先输出变量值检查，再用少量固定数据逐步验证每一步的结果。',
 '（2）switch 的每个 case 末尾都写上 break，default 也写上 break，养成固定的书写习惯；分支较多时先画流程图，确认每个分支的出口。',
 '（3）逻辑表达式按运算优先级加括号，先把“是/否”的判断条件用自然语言写清楚，再翻译成代码；处理“先累加再判断”的业务时，按业务顺序先更新余额再判断积分。',
 '（4）强制类型转换只作用于紧跟其后的表达式，要写成 (int)(amount/100.0f)，用括号把整个表达式括起来，避免 (int)amount/100 这样的错误。',
 '（5）心得：动手编码前先把分支用自然语言或流程图理清楚，可以少走很多弯路；if 与 switch 各有适用场景，范围判断用 if，等值判断用 switch；测试时既要测正常数据，也要测边界值和非法输入，这样才能保证程序的正确性和健壮性。',
],
}

# ---------------------------------------------------------------- helpers ---
def set_font(run, ascii_font, ea_font, size_pt, bold=False):
    run.font.name = ascii_font
    run.font.size = Pt(size_pt)
    run.bold = bold
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn('w:rFonts'))
    if rfonts is None:
        rfonts = rpr.makeelement(qn('w:rFonts'), {})
        rpr.insert(0, rfonts)
    rfonts.set(qn('w:ascii'), ascii_font)
    rfonts.set(qn('w:hAnsi'), ascii_font)
    rfonts.set(qn('w:eastAsia'), ea_font)
    rfonts.set(qn('w:cs'), ascii_font)


def body_format(p, first_indent=Pt(24)):
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.first_line_indent = first_indent
    pf.left_indent = Pt(0)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(BODY_LINE)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY


def code_format(p):
    pf = p.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf.first_line_indent = Pt(0)
    pf.left_indent = Pt(24)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.line_spacing = Pt(CODE_LINE)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY


def add_par_after(cell, anchor_el, style='Body Text'):
    p = cell.add_paragraph(style=style)
    el = p._element
    anchor_el.addnext(el)
    return p, el


def clear_placeholders(cell, marker_el, last_el, keep_last):
    """Collect the empty paragraphs between marker_el and last_el."""
    doomed = []
    cur = marker_el.getnext()
    while cur is not None and cur is not last_el:
        nxt = cur.getnext()
        if cur.tag == qn('w:p'):
            has_drawing = cur.find('.//' + qn('w:drawing')) is not None
            if ''.join(cur.itertext()).strip() or has_drawing:
                break
            doomed.append(cur)
        else:
            break
        cur = nxt
    if keep_last and doomed:
        last_p = cell.paragraphs[-1]._element
        if last_p in doomed:
            doomed.remove(last_p)
    return doomed


def nth_marker(cell, prefix, n):
    count = 0
    for p in cell.paragraphs:
        if p.text.strip().startswith(prefix):
            count += 1
            if count == n:
                return p
    return None


def fill(cell, start_prefix, stop_prefix, items, nth=1):
    """Replace the empty placeholder paragraphs after the nth `start_prefix`."""
    start = nth_marker(cell, start_prefix, nth)
    if start is None:
        raise SystemExit('marker not found: %r #%d' % (start_prefix, nth))

    stop = None
    if stop_prefix:
        stop = nth_marker(cell, stop_prefix, nth)
        if stop is None:
            raise SystemExit('stop marker not found: %r #%d' % (stop_prefix, nth))

    stop_el = stop._element if stop is not None else None
    keep_last = stop is None
    doomed = clear_placeholders(cell, start._element, stop_el, keep_last)
    for el in doomed:
        el.getparent().remove(el)

    anchor = start._element
    made = []
    for kind, value in items:
        style = 'Body Text' if kind == 'text' else 'Normal'
        p, el = add_par_after(cell, anchor, style)
        anchor = el
        made.append((kind, p, el))
        if kind == 'text':
            body_format(p)
            run = p.add_run(value)
            set_font(run, 'Times New Roman', CN, BODY_PT)
        elif kind == 'code':
            code_format(p)
            run = p.add_run(value if value else '')
            set_font(run, CODE_FONT, CN, CODE_PT)
        elif kind == 'blank':
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = Pt(6)
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        elif kind == 'image':
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf = p.paragraph_format
            pf.first_line_indent = Pt(0)
            pf.left_indent = Pt(0)
            pf.space_before = Pt(6)
            pf.space_after = Pt(6)
            pf.line_spacing_rule = WD_LINE_SPACING.SINGLE
            iw, ih = Image.open(value).size
            box_w, box_h = Mm(140), Mm(115)
            scale = min(box_w / iw, box_h / ih)
            run = p.add_run()
            run.add_picture(value, width=Emu(int(iw * scale)), height=Emu(int(ih * scale)))
    return made


def code_items(src_name):
    text = io.open(os.path.join(BASE, src_name), encoding='gbk').read()
    lines = text.replace('\r\n', '\n').split('\n')
    while lines and lines[-1].strip() == '':
        lines.pop()
    return [('code', l) for l in lines]


def shot_items(n):
    return [('image', os.path.join(SHOTS, 'task%d.png' % n))]


# ---------------------------------------------------------------- run ------
if not os.path.exists(BACKUP):
    shutil.copyfile(DOC_IN, BACKUP)
doc = docx.Document(DOC_IN)
table = doc.tables[1]
cell3 = table.rows[3].cells[0]
cell4 = table.rows[4].cells[0]

for n in range(1, 7):
    # (1) 任务分析
    items = [('text', t) for t in TASK[n]]
    items.append(('blank', None))
    fill(cell3, '（1）任务分析', '（2）代码如下：', items, nth=n)
    # (2) 代码如下：
    fill(cell3, '（2）代码如下：', '（3）编译与运行',
         code_items(SRC[n]) + [('blank', None)], nth=n)
    # (3) 编译与运行：截图如下：
    fill(cell3, '（3）编译与运行', None, shot_items(n) + [('blank', None)], nth=n)

# 四、总结
fill(cell4, '1.实验结果分析：', '2.问题：', [('text', t) for t in SUMMARY['1.实验结果分析：']])
fill(cell4, '2.问题：', '3.解决方法及心得：', [('text', t) for t in SUMMARY['2.问题：']])
fill(cell4, '3.解决方法及心得：', None, [('text', t) for t in SUMMARY['3.解决方法及心得：']])

# keep the "（2）代码如下：" / "（3）编译与运行" labels with what follows them
for prefix in ('（2）代码如下：', '（3）编译与运行'):
    for p in cell3.paragraphs:
        if p.text.strip().startswith(prefix):
            p.paragraph_format.keep_with_next = True

# 成绩评定 row must not be split across pages
tr = table.rows[5]._tr
trPr = tr.get_or_add_trPr()
if trPr.find(qn('w:cantSplit')) is None:
    trPr.insert(0, trPr.makeelement(qn('w:cantSplit'), {}))

doc.save(DOC_OUT)
print('saved', DOC_OUT)
