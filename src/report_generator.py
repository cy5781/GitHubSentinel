# src/report_generator.py

import os
from datetime import date, timedelta
from logger import LOG  # 导入日志模块，用于记录日志信息

class ReportGenerator:
    def __init__(self, llm,report_types):
        self.llm = llm  # 初始化时接受一个LLM实例，用于后续生成报告
        self.report_types = report_types
        self.prompts = {}  # 存储所有预加载的提示信息
        self._preload_prompts()

    def _preload_prompts(self):
        """
        预加载所有可能的提示文件，并存储在字典中。
        """
        for report_type in self.report_types:  # 使用从配置中加载的报告类型
            prompt_file = f"../prompts/{report_type}_{self.llm.model}_prompt.txt"
            if not os.path.exists(prompt_file):
                LOG.error(f"提示文件不存在: {prompt_file}")
                raise FileNotFoundError(f"提示文件未找到: {prompt_file}")
            with open(prompt_file, "r", encoding='utf-8') as file:
                self.prompts[report_type] = file.read()

    def generate_daily_report(self, markdown_file_path):
        # 读取Markdown文件并使用LLM生成日报
        with open(markdown_file_path, 'r') as file:
            markdown_content = file.read()

        report = self.llm.generate_daily_report(markdown_content)  # 调用LLM生成报告

        report_file_path = os.path.splitext(markdown_file_path)[0] + "_report.md"
        with open(report_file_path, 'w+') as report_file:
            report_file.write(report)  # 写入生成的报告

        LOG.info(f"GitHub 项目报告已保存到 {report_file_path}")

        return report, report_file_path


    def generate_report_by_date_range(self, markdown_file_path, days):
        # 生成特定日期范围的报告，流程与日报生成类似
        with open(markdown_file_path, 'r') as file:
            markdown_content = file.read()

        report = self.llm.generate_daily_report(markdown_content)

        report_file_path = os.path.splitext(markdown_file_path)[0] + f"_report.md"
        with open(report_file_path, 'w+') as report_file:
            report_file.write(report)
        
        LOG.info(f"GitHub 项目报告已保存到 {report_file_path}")

        return report, report_file_path

