from gdeploy.gcloud.cmd import flag_arg, string_arg, map_arg, listmap_arg, Cmd
import unittest.mock as mock


def test_flag_arg():
    f_arg = flag_arg("allow-unauthenticated")
    expected = ["--allow-unauthenticated"]
    actual = f_arg()
    assert expected == actual


def test_string_arg():
    s_arg = string_arg("entry-point")
    expected = ["--entry-point=hello_http"]
    actual = s_arg("hello_http")
    assert expected == actual


def test_map_arg():
    m_arg = map_arg("update-labels")
    # should come back as sorted by key
    expected = ["--update-labels", "a=yyyy-mm-dd,c=#$@#$!,x=gdeploy"]
    actual = m_arg({"x": "gdeploy", "a": "yyyy-mm-dd", "c": "#$@#$!"})
    assert expected == actual


def test_listmap_arg():
    lm_arg = listmap_arg("remove-labels")
    expected = ["--remove-labels=[label1,label2]"]
    actual = lm_arg(["label1", "label2"])
    assert expected == actual


def test_cmd_simple():

    expected = ["gcloud", "alpha", "functions", "list"]

    with mock.patch("gdeploy.term.run_cmd") as run:
        g = Cmd("alpha", "functions", "list")
        g.run()
        run.assert_called_with(expected)


def test_cmd_complex():

    expected = [
        "gcloud",
        "alpha",
        "functions",
        "deploy",
        "--entry-point=hello_http",
        "--update-labels",
        "deployed_by=gdeploy,deployed_on=yyyy-mm-dd",
        "--remove-labels=[label1,label2]",
        "--allow-unauthenticated",
    ]

    map_args = {
        "entry-point": "hello_http",
        "update-labels": {"deployed_by": "gdeploy", "deployed_on": "yyyy-mm-dd"},
        "remove-labels": ["label1", "label2"],
    }

    flag_args = ["allow-unauthenticated"]

    with mock.patch("gdeploy.term.run_cmd") as run:

        g = Cmd("alpha", "functions", "deploy")
        g.run(map_args, flag_args)
        run.assert_called_with(expected)
