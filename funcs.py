import re


def c_main_compile(ref_out, ref_err, stu_out, stu_err):
    return "error" not in stu_err


def runtime_err_exists(stu_err):
    clean_stu_err = stu_err.strip()
    return clean_stu_err == ""


def p1_relaxed_1022_check(ref_out, ref_err, stu_out, stu_err):
    clean_ref_err = ref_err.strip()
    clean_stu_err = stu_err.strip()
    clean_stu_err = clean_stu_err.replace(" ", "")
    return "1022clone" in clean_stu_err


def p1_relaxed_1024_check(ref_out, ref_err, stu_out, stu_err):
    clean_ref_err = ref_err.strip()
    clean_stu_err = stu_err.strip()
    clean_stu_err = clean_stu_err.replace(" ", "")
    return "1024clone" in clean_stu_err


def p1_strict_check(ref_out, ref_err, stu_out, stu_err):
    clean_ref_err = ref_err.strip()
    clean_stu_err = stu_err.strip()
    clean_stu_err = clean_stu_err.replace(" ", "")
    return "1023clone" in clean_stu_err


def p2_strict_check(ref_out, ref_err, stu_out, stu_err):
    clean_ref_out = ref_out.strip()
    clean_stu_out = stu_out.strip()

    lines = clean_ref_out.split("\n")
    del lines[1:4]
    clean_ref_out = "\n".join(lines)

    lines = clean_stu_out.split("\n")
    if len(lines) > 3:
       del lines[1:4]
       clean_stu_out = "\n".join(lines)
    
    clean_stu_out = clean_stu_out.replace(" ", "")
    clean_stu_out = clean_stu_out.replace("\n", "")
    clean_stu_out = clean_stu_out.replace("\r", "")
    clean_stu_out = clean_stu_out.replace("\t", "")

    clean_ref_out = clean_ref_out.replace(" ", "")
    clean_ref_out = clean_ref_out.replace("\n", "")
    clean_ref_out = clean_ref_out.replace("\r", "")
    clean_ref_out = clean_ref_out.replace("\t", "")

    clean_stu_out = clean_stu_out.lower()
    clean_ref_out = clean_ref_out.lower()

    return clean_stu_out == clean_ref_out


def p2_relaxed_check1(ref_out, ref_err, stu_out, stu_err):
    clean_stu_out = stu_out.strip()
    clean_stu_out = clean_stu_out.replace(" ", "")
    clean_stu_out = clean_stu_out.replace("\n", "")
    clean_stu_out = clean_stu_out.replace("\r", "")
    clean_stu_out = clean_stu_out.replace("\t", "")
    clean_stu_out = clean_stu_out.lower()

    return "10/usr/lib/systemd/systemd" in clean_stu_out


def p2_relaxed_check2(ref_out, ref_err, stu_out, stu_err):
    clean_stu_out = stu_out.strip()
    clean_stu_out = clean_stu_out.replace(" ", "")
    clean_stu_out = clean_stu_out.replace("\n", "")
    clean_stu_out = clean_stu_out.replace("\r", "")
    clean_stu_out = clean_stu_out.replace("\t", "")
    clean_stu_out = clean_stu_out.lower()
    # Change on each boot!!!
    return "17101/usr/lib/systemd/systemd" in clean_stu_out


def p2_perf(ref_out, ref_err, stu_out, stu_err):
    return True


def p3_relaxed_check(ref_out, ref_err, stu_out, stu_err):
    if ref_err != stu_err:
        return False

    pattern = r'\b\d+\b'
    matches = re.findall(pattern, ref_out)
    result = ''.join(matches)

    return result in stu_out


def p3_perf(ref_out, ref_err, stu_out, stu_err):
    return True


def p4_perf(ref_out, ref_err, stu_out, stu_err):
    return True


def p4_relaxed_check(ref_out, ref_err, stu_out, stu_err):
    if ref_err != stu_err:
        return False
    clean_ref_out = ref_out.strip()
    clean_stu_out = stu_out.strip()

    if clean_ref_out in clean_stu_out:
        return True
    return False


def p4_strict_check(ref_out, ref_err, stu_out, stu_err):
    if ref_err != stu_err:
        return False
    clean_ref_out = ref_out.strip()
    clean_stu_out = stu_out.strip()
    return clean_stu_out == clean_ref_out


def p4_no_arg(ref_out, ref_err, stu_out, stu_err):
    if "ello" in stu_out:
        return False
    if "orld" in stu_out:
        return False
    return runtime_err_exists(stu_err)


def p4_two_arg(ref_out, ref_err, stu_out, stu_err):
    if "ello" in stu_out:
        return False
    if "orld" in stu_out:
        return False
    return runtime_err_exists(stu_err)


def p4_str_arg(ref_out, ref_err, stu_out, stu_err):
    if "ello" in stu_out:
        return False
    if "orld" in stu_out:
        return False
    return runtime_err_exists(stu_err)


def p4_perf(ref_out, ref_err, stu_out, stu_err):
    return True

