# TableShare

TableShare 是一个轻量级的 Python 库，用于从网页中提取表格数据并转换为 pandas DataFrame。它支持从在线资源和本地 HTML 文件中抓取表格。

## 安装

你可以通过 pip 安装 TableShare：

```bash
pip install tableshare
使用方法
从在线资源抓取表格
from tableshare import fetch_table, fetch_all_tables

# 抓取单个表格
url = 'http://example.com/table-page'
table_data = fetch_table(url, table_index=0)
print(table_data)

# 抓取所有表格
for table in fetch_all_tables(url):
    print(table)
从本地 HTML 文件抓取表格
from tableshare import fetch_all_tables_locally, fetch_table_locally

# 抓取本地文件中的所有表格
html_file_path = 'path_to_your_local_file.html'
fetch_all_tables_locally(html_file_path)

# 抓取本地文件中的指定表格
table_index = 0  # 指定表格索引
table_data = fetch_table_locally(html_file_path, table_index)
print(table_data)
功能
从网页中抓取单个或所有表格。
从本地 HTML 文件中抓取单个或所有表格。
将抓取的表格数据转换为 pandas DataFrame，便于进一步分析和处理。
注意事项
确保在抓取在线资源时，目标网站的 robots.txt 允许爬虫访问。
对于动态加载的表格数据，可能需要使用如 Selenium 等工具来获取完整的页面内容。
对于本地文件的处理，确保文件路径正确且文件可读。
贡献
如果你在使用过程中发现任何问题或有改进建议，请在 GitHub 仓库中提交 issue 或 pull request。

许可证
TableShare 遵循 MIT 许可证。有关详细信息，请参见 LICENSE 文件。

联系
如果你有任何问题或需要帮助，请通过以下方式联系我们：

电子邮件：baiguanba@outlook.com
GitHub 仓库：https://github.com/yourusername/tableshare

请确保将上述 `README.md` 中的占位符（如 `http://example.com/table-page`、`path_to_your_local_file.html`、`your.email@example.com`、`yourusername` 等）替换为实际的值。此外，如果你的库有特定的依赖项或其他安装要求，也应该在 `README.md` 中提及。