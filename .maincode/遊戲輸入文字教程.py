import pygame
import math
import sys

# 初始化
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("how")
clock = pygame.time.Clock()
font = pygame.font.Font("金陵.ttf", 40)  # 使用系统默认字体（安卓上兼容中文）

# 输入框位置和状态
input_rect = pygame.Rect(100, 200, 600, 60)
input_text = ""       # 存储输入的字符
active = False        # 是否处于输入状态
cursor_visible = True # 光标闪烁状态
cursor_timer = 0      # 光标计时器

# 提示信息
hint_text = "點擊輸入框開始打字！"

def main():
    global input_text, active, cursor_visible, cursor_timer

    running = True
    while running:
        # 计算帧间隔时间（用于光标闪烁）
        dt = clock.tick(60)

        # --- 事件处理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 点击输入框
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                    pygame.key.start_text_input()  # 关键：开启输入并唤起安卓软键盘
                else:
                    active = False
                    pygame.key.stop_text_input()   # 点击外部，关闭软键盘

            # 键盘输入事件（安卓软键盘发来的也是这个）
            elif event.type == pygame.KEYDOWN and active:
                # 按退格键删除
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                # 按回车键（这里作为提交示例，也可以按需隐藏键盘）
                elif event.key == pygame.K_RETURN:
                    input_text = ""
                    active = False
                    pygame.key.stop_text_input()
                # 接收普通字符（安卓的中文输入法也是发 unicode 字符）
                elif event.unicode and event.unicode.isprintable():
                    input_text += event.unicode

        # --- 光标闪烁逻辑 ---
        cursor_timer += dt
        if cursor_timer >= 500:  # 每 0.5 秒切换
            cursor_visible = not cursor_visible
            cursor_timer = 0

        # --- 绘制画面 ---
        screen.fill((30, 30, 30))  # 深灰色背景

        # 绘制输入框背景
        pygame.draw.rect(screen, (60, 60, 60), input_rect, border_radius=10)
        # 绘制边框（激活时为青色，未激活为灰色）
        if active:
            pygame.draw.rect(screen, (0, 200, 255), input_rect, 2, border_radius=10)
        else:
            pygame.draw.rect(screen, (100, 100, 100), input_rect, 2, border_radius=10)

        # 渲染已经输入的文字
        text_surf = font.render(input_text, True, (255, 255, 255))
        
        # 文字太宽时，让它向左滑动（防止超出输入框）
        max_text_width = input_rect.width - 20
        if text_surf.get_width() > max_text_width:
            offset_x = text_surf.get_width() - max_text_width
            screen.blit(text_surf, (input_rect.x + 10 - offset_x, input_rect.y + 10))
        else:
            screen.blit(text_surf, (input_rect.x + 10, input_rect.y + 10))

        # 绘制光标（输入框激活且闪烁时显示）
        if active and cursor_visible:
            cursor_x = input_rect.x + 10 + text_surf.get_width() + 2
            # 确保光标不超出输入框
            if cursor_x < input_rect.right - 10:
                pygame.draw.line(screen, (255, 255, 255), 
                                 (cursor_x, input_rect.y + 10), 
                                 (cursor_x, input_rect.y + 50), 2)

        # 绘制提示文字（没输入时显示）
        if not input_text:
            hint_surf = font.render(hint_text, True, (150, 150, 150))
            screen.blit(hint_surf, (input_rect.x + 10, input_rect.y + 10))

        # 更新画面
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()