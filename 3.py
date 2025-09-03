import os
import re

def extract_chinese_text(input_folder, output_folder):
    """
    从输入文件夹中提取所有文件的中文文本，每个文件生成单独的中文文本文件
    
    参数:
    input_folder (str): 包含源文件的文件夹路径
    output_folder (str): 存放中文提取结果的文件夹路径
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 遍历输入文件夹中的所有文件
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        
        # 只处理文件（跳过子文件夹）
        if os.path.isfile(input_path):
            try:
                # 读取文件内容（UTF-8编码）
                with open(input_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 提取所有中文文本（包括标点符号）
                # 匹配规则：连续的中文字符、中文标点、数字、英文字母（作为专有名词保留）
                chinese_blocks = re.findall(
                    r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]+'
                    r'(?:[\w\s,.;:()\'"?!@#$%^&*_+\-=\[\]{}|\\<>`~]*'
                    r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]+)*',
                    content
                )
                
                # 如果找到中文内容
                if chinese_blocks:
                    # 清理内容：移除纯英文行、多余空行
                    cleaned_lines = []
                    for block in chinese_blocks:
                        lines = block.strip().split('\n')
                        for line in lines:
                            # 跳过纯英文行（但保留包含中文的混合行）
                            if re.search(r'[\u4e00-\u9fff]', line):
                                # 移除行首尾空白
                                cleaned_line = line.strip()
                                if cleaned_line:
                                    cleaned_lines.append(cleaned_line)
                    
                    # 生成输出文件路径
                    output_path = os.path.join(output_folder, f"zh_{filename}")
                    
                    # 写入中文内容
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write('\n'.join(cleaned_lines))
                    
                    print(f"已处理: {filename} -> {os.path.basename(output_path)}")
                else:
                    print(f"跳过无中文内容: {filename}")
            
            except Exception as e:
                print(f"处理文件 {filename} 时出错: {str(e)}")

if __name__ == "__main__":
    # 配置输入输出文件夹
    input_folder = "C:\\04_Users\Desktop\Study\\01_Crash Course\Crash-Course-Computer-Science-Chinese\(字幕)全40集中英字幕文本"    # 存放源文件的文件夹
    output_folder = "C:\\04_Users\Desktop\Study\\01_Crash Course\Crash-Course-Computer-Science-Chinese\zh_text"  # 存放中文提取结果的文件夹
    
    extract_chinese_text(input_folder, output_folder)
    print("\n处理完成！中文文本已保存到:", os.path.abspath(output_folder))