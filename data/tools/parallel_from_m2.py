import argparse

SKIP = {"noop", "UNK", "Um"}

# Apply the edits of a single annotator to orig to generate corrected sentences.
def main(args):
    m2 = open(args.m2_file).read().strip().split("\n\n")
    out = open(args.out, "w")
    # Do not apply edits with these error types

    for sent in m2:
        sent = sent.split("\n")
        err_sent = " ".join(sent[0].split()[1:]) # Ignore "S "
        edits = sent[1:]

        if not args.all:
            out_sent = apply_edits(sent, edits, args.id)
            out.write(err_sent+"\t"+out_sent+"\n")
        else:
            coder_ids = extract_ids(edits)
            for coderid in coder_ids:
                out_sent = apply_edits(sent, edits, coderid)
                out.write(err_sent+"\t"+out_sent+"\n")


def extract_ids(edits):
    ids = set()
    for edit in edits:
        edit = edit.split("|||")
        ids.add(int(edit[-1]))
    if not ids:
        ids.add(0)
    return ids


def apply_edits(sent, edits, coderid):
    cor_sent = sent[0].split()[1:] # Ignore "S "
    offset = 0
    for edit in edits:
        edit = edit.split("|||")
        if edit[1] in SKIP: continue # Ignore certain edits
        coder = int(edit[-1])
        if coder != coderid: continue # Ignore other coders
        span = edit[0].split()[1:] # Ignore "A "
        start = int(span[0])
        end = int(span[1])
        cor = edit[2].split()
        cor_sent[start+offset:end+offset] = cor
        offset = offset-(end-start)+len(cor)
    if not cor_sent:
        cor_sent = sent[0].split()[1:] # Ignore "S "
    return " ".join(cor_sent)


if __name__ == "__main__":
    # Define and parse program input
    parser = argparse.ArgumentParser()
    parser.add_argument("m2_file",  help="The path to an input m2 file.")
    parser.add_argument("-out",     help="A path to where we save the combined m2 file.", required=True)
    parser.add_argument("-id",      help="The id of an annotator in the m2 file.", type=int, default=0)
    parser.add_argument("-all",     help="Extract corrected sentences from all annotators.", action='store_true')
    args = parser.parse_args()
    main(args)
