from argparse import ArgumentParser, ArgumentTypeError
import re

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
ul, .root {{
    list-style-type: none;
}}

.root {{
  margin: 0;
  padding: 0;
}}

.caret {{
  cursor: pointer;
  user-select: none;
}}

.caret::before {{
  content: "\\25B6";
  color: black;
  display: inline-block;
  margin-right: 6px;
}}

.caret-down::before {{
  transform: rotate(90deg);
}}

.nested {{
  display: none;
}}

.active {{
  display: block;
}}

.hide-btn {{
      margin-left: 20px;
}}

li {{
  margin-top: 10px;
}}

.regular-usage {{
  color: black;
}}

.high-usage {{
  color: red;
}}
</style>
</head>
<body>
    <ul class="root">
        {0}
    </ul>

    <script>
        var toggler = document.getElementsByClassName("caret");
        var i;

        for (i = 0; i < toggler.length; i++) {{
          toggler[i].addEventListener("click", function() {{
            this.parentElement.querySelector(".nested").classList.toggle("active");
            this.classList.toggle("caret-down");
          }});
        }}
        var items = document.getElementsByClassName('hide-btn');

        for (i = 0; i < items.length; ++i) {{
          items[i].onclick = e => {{
            li = e.target.parentElement;
            if (li.style.backgroundColor != 'rgba(0, 0, 0, 0.5)') {{
              li.style.backgroundColor = 'rgba(0, 0, 0, 0.5)'
            }} else {{
              li.style.backgroundColor = 'transparent'
            }}
          }}
        }}
    </script>

</body>
</html>
"""

def check_percentage(value):
    percentage = float(value)
    if percentage < 0 or percentage > 100:
        raise ArgumentTypeError("%s is an invalid percentage with floating point value" % value)
    return percentage

def percents_to_value(percentage_string):
  return float(percentage_string.strip('%'))

def get_line_data(line):
    pattern = re.compile("\[*(?P<comment>.*?)] *(?P<data>.*)")
    match = pattern.match(line)

    comment = match.group("comment").strip()
    data = match.group("data").split()

    i = depth = 0

    while data[i] == '|':
        i += 1
        depth += 1

    i += 1

    summary = ' '.join(reversed(data[i:]))

    return (depth, summary, comment)

def create_ul(landmarks, threshold):
    res = ""
    f = open(landmarks, "r")

    line = f.readline()
    close = []

    while True:
        next_line = f.readline()

        d, s, c = get_line_data(line)

        li_classes = 'high-usage' if threshold and percents_to_value(s.split(':')[-1]) >= threshold else 'regular-usage'

        if not next_line:
            res += f'<li class="{li_classes}">{s} ({c})</li>'
            while len(close):
                res += f'</{close.pop()}>'
            break

        next_d, _, _ = get_line_data(next_line)

        if next_d > d:
            res += f'<li class="{li_classes}"><span class="caret">{s} ({c})</span><button class="hide-btn">Toggle</button>'
            close.append('li')
            res += '<ul class="nested">'
            close.append('ul')
            line = next_line
            continue

        if next_d == d:
            res += f'<li class="{li_classes}">{s} ({c})</li>'
            line = next_line
            continue

        # next_d < d
        res += f'<li class="{li_classes}">{s} ({c})</li>'
        line = next_line
        for _ in range(0, (d - next_d) * 2):
            res += f'</{close.pop()}>'

    return res

def main():
    parser = ArgumentParser(description='Pass in and out files paths with optional threshold to add highlights')
    parser.add_argument('-i', '--in',
                        dest='landmarks',
                        metavar='FILE',
                        help='path to Landmarks summary',
                        required=True)#,
                        #type=lambda x: is_valid_file(parser, x))
    parser.add_argument('-o', '--out',
                        dest='html',
                        metavar='FILE',
                        help='path to html result',
                        required=True)
    parser.add_argument('-t', '--threshold',
                        dest='threshold',
                        metavar='PERCENTAGE',
                        help='threshold for usage percentage for highliting',
                        required=False,
                        type=check_percentage)

    args = parser.parse_args()

    tree = create_ul(args.landmarks, args.threshold)

    html = HTML_TEMPLATE.format(tree)

    f = open(args.html, 'w')
    f.write(html)
    f.close()

if __name__ == '__main__':
    main()
