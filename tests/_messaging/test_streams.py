import sys

from marimo._runtime.runtime import Kernel
from tests.conftest import ExecReqProvider, MockedKernel


# Make sure that standard in is installed; stdin is not writable so we
# just check that its methods are callable and return mocked values.
class TestStdin:
    @staticmethod
    def test_encoding(mocked_kernel: MockedKernel) -> None:
        assert mocked_kernel.stdin.encoding == sys.stdin.encoding

    @staticmethod
    def test_input_installed(k: Kernel, exec_req: ExecReqProvider) -> None:
        k.run([exec_req.get("output = input('hello')")])
        assert k.globals["output"] == "hello"

    @staticmethod
    def test_readline_installed(k: Kernel, exec_req: ExecReqProvider) -> None:
        k.run([exec_req.get("output = sys.stdin.readline()")])
        assert k.globals["output"] == ""

    @staticmethod
    def test_readlines_installed(k: Kernel, exec_req: ExecReqProvider) -> None:
        k.run([exec_req.get("output = sys.stdin.readlines()")])
        assert k.globals["output"] == [""]


class TestStdout:
    @staticmethod
    def test_encoding(mocked_kernel: MockedKernel) -> None:
        assert mocked_kernel.stdout.encoding == sys.stdout.encoding

    @staticmethod
    def test_fileno(k: Kernel, exec_req: ExecReqProvider) -> None:
        k.run([exec_req.get("fileno = sys.stdout.fileno()")])
        assert k.globals["fileno"] is not None

    @staticmethod
    def test_print(
        mocked_kernel: MockedKernel, exec_req: ExecReqProvider
    ) -> None:
        mocked_kernel.k.run([exec_req.get("print('hello'); print('there')")])
        assert mocked_kernel.stdout.messages == ["hello", "\n", "there", "\n"]

    @staticmethod
    def test_write(
        mocked_kernel: MockedKernel, exec_req: ExecReqProvider
    ) -> None:
        mocked_kernel.k.run(
            [exec_req.get("import sys; sys.stdout.write('hello')")]
        )
        assert mocked_kernel.stdout.messages == ["hello"]

    @staticmethod
    def test_writelines(
        mocked_kernel: MockedKernel, exec_req: ExecReqProvider
    ) -> None:
        mocked_kernel.k.run(
            [
                exec_req.get(
                    "import sys; sys.stdout.writelines(['hello', 'there'])"
                )
            ]
        )
        assert mocked_kernel.stdout.messages == ["hello", "there"]


class TestStderr:
    @staticmethod
    def test_encoding(mocked_kernel: MockedKernel) -> None:
        assert mocked_kernel.stderr.encoding == sys.stderr.encoding

    @staticmethod
    def test_fileno(k: Kernel, exec_req: ExecReqProvider) -> None:
        k.run([exec_req.get("fileno = sys.stderr.fileno()")])
        assert k.globals["fileno"] is not None

    @staticmethod
    def test_write(
        mocked_kernel: MockedKernel, exec_req: ExecReqProvider
    ) -> None:
        mocked_kernel.k.run(
            [exec_req.get("import sys; sys.stderr.write('hello')")]
        )
        assert mocked_kernel.stderr.messages == ["hello"]

    @staticmethod
    def test_writelines(
        mocked_kernel: MockedKernel, exec_req: ExecReqProvider
    ) -> None:
        mocked_kernel.k.run(
            [
                exec_req.get(
                    "import sys; sys.stderr.writelines(['hello', 'there'])"
                )
            ]
        )
        assert mocked_kernel.stderr.messages == ["hello", "there"]


def test_import_multiprocessing(
    mocked_kernel: MockedKernel, exec_req: ExecReqProvider
) -> None:
    # https://github.com/marimo-team/marimo/issues/684
    mocked_kernel.k.run(
        [
            exec_req.get(
                """
                from multiprocessing import Manager
                Manager().dict()
                print("hello")
                """
            )
        ]
    )
    assert mocked_kernel.stdout.messages == ["hello", "\n"]
