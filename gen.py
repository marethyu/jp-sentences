import csv

prologue = """<!DOCTYPE html>
<html>
<head>
<title>Essential Japanese Sentences</title>
<link rel="stylesheet" type="text/css" href="style.css" />
</head>
<body>
<h1>Essential Japanese Sentences</h1>
<p>All sentences are extracted from <i>Japanese Sentence Patterns for Effective Communication</i> by Taeko Kamiya</p>
<p>ADVICE: When you study patterns and examples, please "think Japanese." Treat English translations as a <i>tool</i> that help you to think Japanese.</p>
<p>がんばって！<p>
<div id="box-list">
"""

epilogue = """</div>
</body>
</html>
"""

chapters = [
    '<NIL>',
    'Identifying and describing people and things',
    'Describing the existence of animate and inanimate things',
    'Making comparisons',
    'Describing actions in the past, present and future',
    'Actions in progress, completed, successive, simultaneous, miscellaneous',
    'Stating purpose, cause and reason',
    'Commands, requests, suggestions, approval, disapproval, prohibition and obligation',
    'Expressing ability, preference, desire, intent, resolution and experience',
    'Describing the actions of giving and receiving',
    'Expressing conjecture and hearsay, and quoting people',
    'Using conditional, passive, causative and causative-passive',
    'Making relative clauses'
]

internal_links = []

ty_to_str = ['pattern', 'example', 'practice']
counters = [1, 1, 1]

def gen_link(line_buf, ty):
    tag = f'{ty_to_str[ty]}{counters[ty]}'
    counters[ty] += 1
    internal_links.append(tag)
    line_buf.append(f'<a id="{tag}"></a>\n')

def write_text_subbox(line_buf, label, txt):
    line_buf.append('<div class="text-subbox">\n')
    line_buf.append(f'<p>{label}</p>\n')
    line_buf.append(txt + '\n')
    line_buf.append('</div>\n')

def gen_pattern_box(line_buf, chapter, kanji, kana, meaning):
    gen_link(line_buf, 0)
    line_buf.append('<div class="pattern-box">\n')
    line_buf.append('<div class="box-type">Pattern</div>\n')
    write_text_subbox(line_buf, 'Kanji', f'<div class="kanji-sentence">{kanji}</div>')
    write_text_subbox(line_buf, 'Kana', f'<span class="spoiler">{kana}</span>')
    write_text_subbox(line_buf, 'Translation', f'<span class="spoiler">{meaning}</span>')
    line_buf.append(f'<p>Chapter {chapter} ({chapters[int(chapter)]})</p>\n')
    line_buf.append('</div>\n')

def gen_example_box(line_buf, chapter, kanji, kana, meaning):
    gen_link(line_buf, 1)
    line_buf.append('<div class="example-box">\n')
    line_buf.append('<div class="box-type">Example</div>\n')
    write_text_subbox(line_buf, 'Kanji', f'<div class="kanji-sentence">{kanji}</div>')
    write_text_subbox(line_buf, 'Kana', f'<span class="spoiler">{kana}</span>')
    write_text_subbox(line_buf, 'Translation', f'<span class="spoiler">{meaning}</span>')
    line_buf.append(f'<p>Chapter {chapter} ({chapters[int(chapter)]})</p>\n')
    line_buf.append('</div>\n')

def gen_practice_box(line_buf, chapter, kanji, kana, meaning):
    gen_link(line_buf, 2)
    line_buf.append('<div class="practice-box">\n')
    line_buf.append('<div class="box-type">Practice</div>\n')
    write_text_subbox(line_buf, 'Translation', f'<p class="plain-text">{meaning}</p>')
    write_text_subbox(line_buf, 'Kanji', f'<span class="spoiler">{kanji}</span>')
    write_text_subbox(line_buf, 'Kana', f'<span class="spoiler">{kana}</span>')
    line_buf.append(f'<p>Chapter {chapter} ({chapters[int(chapter)]})</p>\n')
    line_buf.append('</div>\n')

with open('jp-sentences.csv', encoding='utf8', mode='r') as csv_file, open('index.html', encoding='utf-8', mode='w') as f:
    csv_reader = csv.DictReader(csv_file)
    f.write(prologue)
    lb = []
    for row in csv_reader:
        if row['Type'][1] == 'a':
            gen_pattern_box(lb, row['Chapter'], row['Kanji'], row['Kana'], row['Meaning'])
        elif row['Type'][1] == 'x':
            gen_example_box(lb, row['Chapter'], row['Kanji'], row['Kana'], row['Meaning'])
        else:
            gen_practice_box(lb, row['Chapter'], row['Kanji'], row['Kana'], row['Meaning'])
    internal_links.sort()
    f.write('<div id="toc">\n')
    f.write('<h2>TOC<h2>\n')
    for name in internal_links:
        f.write(f'<a href="#{name}">{name}</a><br>\n')
    f.write('</div>\n')
    for line in lb:
        f.write(line)
    f.write(epilogue)
