# AWK script used to parse shell scripts, created during TripleO deployments,
# and convert them into rST files for digestion by Sphinx.
#
# General notes:
#
# - Only blocks between `### ---start_docs` and `### ---stop_docs` will be
#     parsed
# - Lines containing `# nodocs` will be excluded from rST output
# - Lines containing `## ::` indicate subsequent lines should be formatted
#     as code blocks
# - Other lines beginning with `## <anything else>` will have the prepended
#     `## ` removed. (This is how you would add general rST formatting)
# - All other lines (including shell comments) will be indented by four spaces

/^### --start_docs/ {
    for (;;) {
        if ((getline line) <= 0)
            unexpected_eof()
        if (line ~ /^### --stop_docs/)
            break
        if (match(line, ".* #nodocs$"))
            continue
        if (substr(line, 0, 5) == "## ::") {
            line = "\n::\n"
        } if (substr(line, 0, 3) == "## ") {
            line = substr(line, 4)
        } else if (line != "") {
            line = "    "line
        }
        print line > "/dev/stdout"
    }
}

function unexpected_eof() {
    printf("%s:%d: unexpected EOF or error\n", FILENAME, FNR) > "/dev/stderr"
    exit 1
}

END {
    if (curfile)
        close(curfile)
}
