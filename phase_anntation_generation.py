def write_comments_to_file(comments):
    with open("F:\\JI\\RESEARCH\\DATABASE\\wanggang\\phase_annotations\\video03.txt", 'w') as f:
        for comment in comments:
            f.write(f"{comment['timestamp']}\t{comment['phase']}\n")


comments = []

# 创建阶段注释
for i in range(1, 215):
    if i < 5:
        comments.append({'timestamp': i, 'phase': "introduction"})
    elif i < 75:
        comments.append({'timestamp': i, 'phase': "BeefPreparation"})
    elif i < 124:
        comments.append({'timestamp': i, 'phase': "FlavourPreparation"})
    elif i < 208:
        comments.append({'timestamp': i, 'phase': "cooking"})
    else:
        comments.append({'timestamp': i, 'phase': "PutDishesIntoPlates"})

# 将注释写入文件
write_comments_to_file(comments)
