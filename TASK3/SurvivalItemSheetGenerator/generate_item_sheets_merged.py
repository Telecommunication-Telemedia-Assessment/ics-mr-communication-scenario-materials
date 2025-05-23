"""
A python module for generating latex documents containing sheets for each participant printed as A6 sheets on A4 paper.
Sheets can be generated for player/participant group sizes of 2,3,4,6.

Usage: python generate_item_sheets_merged.py -v [group_size_version]
"""
#import os
import argparse
import pandas as pd
import os

parser = argparse.ArgumentParser("generate_item_sheets_merged")
parser.add_argument("-v", "--variant", help="Group size variant to generate. Sheets can be generated for player/participant group sizes of 2,3,4,6.", type=str)
args = parser.parse_args()

def generate_item_sheet(participant_id, data, scenario, scenario_desc):
    header = r"""\documentclass{article}
\usepackage{graphicx}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern}
\usepackage{float}
\usepackage{caption}
\usepackage{subcaption}
\usepackage[paperwidth=4.1in, paperheight=5.8in, margin=0.25in]{geometry}
\renewcommand*\familydefault{\sfdefault}
\pagenumbering{gobble}

\begin{document}
    """
    
    footer = r"""
\end{document}
    """
    
    if data is not None:    
        body = r"""
        \par\noindent\rule{\textwidth}{0.4pt}"""
        for item in data.values:
            body += r"""
    \begin{figure}[H]
        \centering
        \begin{minipage}{0.25\textwidth}
            \centering
            \includegraphics[width=\textwidth]{""" + path_imgs+item[0] + r"""}
        \end{minipage}\hfill
        \begin{minipage}{0.7\textwidth}
            \centering
            \Large """ + item[1] + r"""
        \end{minipage}
    \end{figure}
    \vspace{-0.8em}
    \noindent\rule{\textwidth}{0.4pt}
            """
        body += r"""
    \clearpage
    \section*{Scenario: \textmd{"""+scenario.title()+r"""} \hfill Participant \textmd{"""+str(participant_id)+r"""}}
    \Large """ + scenario_desc
    else:
        body = ''
    
    return header, body, footer

def write_latex_file(filename, latex_content):
    with open(filename, 'w') as f:
        f.write(latex_content)

path_lists = "../SurvivalItemData/"
path_imgs = "../SurvivalItemImages/" # in reference to path_out
path_desc = "../Scenarios/"
path_out = "../SurvivalItemSheets/" 

# create output directory if required
if not os.path.exists(path_out):
    os.makedirs(path_out)

# get item lists
list_files = [f for f in os.listdir(path_lists) if f.endswith('.csv')]

num_participants = int(args.variant)

for filename in list_files:
    
    scenario = filename.split('_')[0]

    # read description
    with open(path_desc+f'{scenario}.txt', 'r') as file:
        scenario_description = file.read()

    items = pd.read_csv(path_lists+filename)

    items_per_participant = int(len(items) / num_participants)

    #generate header
    document,_,_ = generate_item_sheet(None, None, None, '') # only header
    document = document.replace(r"\begin{document}", r"""\input{style/print_on_more_pages.tex}
\begin{document}""")

    for p in range(num_participants):
        
        p_items = items.iloc[items_per_participant * p:items_per_participant * (p+1)]

        # generate document body
        _,body,_ = generate_item_sheet(p, p_items, scenario, scenario_description)
        document += body
        document += r'\clearpage'

    document += r"""
        \end{document}
        """
    
    # write to file
    texfile = path_out+f'{args.variant}p_{scenario}_merged.tex'
    write_latex_file(f'{texfile}', document)
            
    # compile pdf
    os.system(f'pdflatex -output-directory {path_out} {texfile}')