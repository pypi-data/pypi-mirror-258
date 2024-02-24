"""
Work wechat log notify.
"""
from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

setup(
    name='work_wechat_log_notify',
    packages=find_packages(include=["src"]),
    package_dir={"": "src"},
    package_data={"": ["LICENSE"]},
    version='0.1.0',
    description='Work wechat log notify.',
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://gitee.com/temporary-worker-team/work_wechat_log_notify",
    author='kingsword09',
    license='MIT',
    project_urls={
        "Documentation": "https://gitee.com/temporary-worker-team/work_wechat_log_notify",
        "Source": "https://gitee.com/temporary-worker-team/work_wechat_log_notify",
    },
    install_requires=[
        "requests", "tabulate"
    ],
)
