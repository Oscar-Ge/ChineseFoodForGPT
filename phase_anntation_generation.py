def write_comments_to_file(c):
    """
    Write comments to a file.
    Args:
        c (list): A list of comments to be written to the file.
    Returns:
        None
    """
    with open("F:\\JI\\RESEARCH\\DATABASE\\wanggang\\ChineseFoodForGPT\\phase_annotations\\video04.txt", 'w') as f:
        for comment in c:
            f.write(f"{comment['timestamp']}\t{comment['phase']}\n")


comments = []

# 创建阶段注释
for i in range(1, 168):
    if i < 5:
        comments.append({'timestamp': i, 'phase': "introduction"})
    elif i < 90:
        comments.append({'timestamp': i, 'phase': "Preparation"})
    elif i < 155:
        comments.append({'timestamp': i, 'phase': "cooking"})
    else:
        comments.append({'timestamp': i, 'phase': "PutDishesIntoPlates"})

# 将注释写入文件
write_comments_to_file(comments)
