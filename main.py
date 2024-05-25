# 需命令行:'py -m pip install pygame' 或 'pip install pygame'
import pygame
import time, random
# import os

pygame.init()
# 初始化pygame

# img = pygame.image.load("rect/icon.ico")
# pygame.display.set_icon(img)

size = (1000, 700)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Rect")
# 初始化窗口

fps = pygame.time.Clock()
fps.tick(60)
# 设置帧率

white = (255, 255, 255)
# 定义颜色

done = True

font = pygame.font.SysFont('Arial', 24)

def start_menu():
    global done
    screen.fill((0, 0, 0))
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
        #退出事件检测
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_s]:
            game()
        elif pressed[pygame.K_q]:
            done = False
        #开始游戏

        text1 = font.render("Press S to start", True, white)
        text2 = font.render("Press Q to quit the game", True, white)

        screen.blit(text1, (450, 300))
        screen.blit(text2, (450, 400))
        pygame.display.update()

def game():
    global done

    start_time = time.time()
    left_time = 100
    catch_CD = 0
    escape_CD = 0
    CD_last_time = start_time
    CD_this_time = start_time
    # 设置计时器

    rect_x_p1 = 50
    rect_y_p1 = 600
    rect_x_p2 = 900
    rect_y_p2 = 600
    rect_height = 50
    rect_width = 50
    # 对象的初始数据

    catch = bool(random.getrandbits(1))

    bouncy = False
    # 设成True有彩蛋

    y_speed_p1 = 0
    x_speed_p1 = 0
    y_speed_p2 = 0
    x_speed_p2 = 0
    bounce_height_p1 = 0
    bounce_height_p2 = 0
    # 速度初始化

    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
            # 退出事件检测

        CD_this_time = time.time()
        catch_CD -= CD_this_time - CD_last_time
        escape_CD -= CD_this_time - CD_last_time
        CD_last_time = time.time()
        if catch_CD < 0.0:
            catch_CD = 0.0
        if escape_CD < 0.0:
            escape_CD = 0.0
        # 技能计时器

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_d]:
            if x_speed_p1 < 0.5:
                x_speed_p1 += 0.0005
        elif pressed[pygame.K_a]:
            if x_speed_p1 > -0.5:
                x_speed_p1 -= 0.0005
        elif x_speed_p1 < -0.001 or x_speed_p1 > 0.001:
            if x_speed_p1 > 0:
                x_speed_p1 -= 0.0005
            if x_speed_p1 < 0:
                x_speed_p1 += 0.0005
        else:
            x_speed_p1 = 0
        # P1的横向移动

        if pressed[pygame.K_w] and y_speed_p1 == 0:
            y_speed_p1 = -0.8
            rect_y_p1 -= 0.1
            if bouncy:
                bounce_height_p1 = -0.8
        # P1的跳跃

        if pressed[pygame.K_s]:
            y_speed_p1 = 1.0
        # P1的潜行

        if pressed[pygame.K_q] and catch and catch_CD == 0.0:
            rect_y_p1 = rect_y_p2 - 300
            rect_x_p1 = rect_x_p2
            y_speed_p1 = 0.0
            catch_CD = 10.0
        # P1的传送技能

        if pressed[pygame.K_q] and not (catch) and escape_CD == 0.0:
            y_speed_p2 = -2.0
            escape_CD = 10.0
            rect_y_p2 -= 0.1
            # P1的放飞技能

        if pressed[pygame.K_RIGHT]:
            if x_speed_p2 < 0.5:
                x_speed_p2 += 0.0005
        elif pressed[pygame.K_LEFT]:
            if x_speed_p2 > -0.5:
                x_speed_p2 -= 0.0005
        elif x_speed_p2 < -0.001 or x_speed_p2 > 0.001:
            if x_speed_p2 > 0:
                x_speed_p2 -= 0.0005
            if x_speed_p2 < 0:
                x_speed_p2 += 0.0005
        else:
            x_speed_p2 = 0
        # P2的横向移动

        if pressed[pygame.K_UP] and y_speed_p2 == 0:
            y_speed_p2 = -0.8
            rect_y_p2 -= 0.1
            if bouncy:
                bounce_height_p2 = -0.8
        # P2的跳跃

        if pressed[pygame.K_DOWN]:
            y_speed_p2 = 1.0
        # P2的潜行

        if pressed[pygame.K_SLASH] and (not catch) and catch_CD == 0.0:
            rect_y_p2 = rect_y_p1 - 300
            rect_x_p2 = rect_x_p1
            y_speed_p2 = 0.0
            catch_CD = 10.0
        # P2的传送技能

        if pressed[pygame.K_SLASH] and catch and escape_CD == 0.0:
            y_speed_p1 = -2.0
            rect_y_p1 -= 0.1
            escape_CD = 10.0
        # P2的放飞技能

        if rect_y_p1 >= 625:
            if bounce_height_p1 > -0.2:
                y_speed_p1 = 0
                rect_y_p1 = 625
            elif bouncy:
                bounce_height_p1 = bounce_height_p1 * 0.8
                rect_y_p1 -= 0.1
                y_speed_p1 = bounce_height_p1
        else:
            y_speed_p1 += 0.001

        if rect_y_p2 >= 625:
            if bounce_height_p2 > -0.2:
                y_speed_p2 = 0
                rect_y_p2 = 625
            elif bouncy:
                bounce_height_p2 = bounce_height_p2 * 0.8
                rect_y_p2 -= 0.1
                y_speed_p2 = bounce_height_p2
        else:
            y_speed_p2 += 0.001
        # 重力模拟

        if rect_x_p1 >= 925:
            x_speed_p1 = 0
            rect_x_p1 = 924.999
        elif rect_x_p1 <= 25:
            x_speed_p1 = 0
            rect_x_p1 = 25.001

        if rect_x_p2 >= 925:
            x_speed_p2 = 0
            rect_x_p2 = 924.999
        elif rect_x_p2 <= 25:
            x_speed_p2 = 0
            rect_x_p2 = 25.001
        # 惯性模拟 边缘检测

        rect_y_p1 += y_speed_p1
        rect_x_p1 += x_speed_p1

        rect_y_p2 += y_speed_p2
        rect_x_p2 += x_speed_p2
        # 移动执行

        if rect_x_p1 <= rect_x_p2 + 50 \
                and rect_x_p1 >= rect_x_p2 - 50 \
                and rect_y_p1 <= rect_y_p2 + 50 \
                and rect_y_p1 >= rect_y_p2 - 50:
            catch = not catch
            rect_x_p1 = 50
            rect_y_p1 = 600
            rect_x_p2 = 900
            rect_y_p2 = 600
            catch_CD = 0.0
            escape_CD = 0.0
        # 碰撞检测

        if catch:
            text1 = font.render("Catcher: Black", True, white)
        else:
            text1 = font.render("Catcher: White", True, white)
        # 设置抓逃轮次文字

        this_time = left_time - (time.time() - start_time)
        str_time = str(round(this_time))
        text2 = font.render(str_time, True, white)
        # 计时器

        text3 = font.render("catch CD:" + str(round(catch_CD, 1)), True, white)
        text4 = font.render("escape CD:" + str(round(escape_CD, 1)), True, white)
        # 技能CD绘制

        if this_time <= 0:
            break
        # 时长判断(是否结束)

        screen.fill((0, 0, 0))
        screen.blit(text1, (450, 10))
        screen.blit(text2, (450, 30))
        screen.blit(text3, (700, 30))
        screen.blit(text4, (700, 50))
        pygame.draw.rect(screen, white, [rect_x_p1, rect_y_p1, rect_width, rect_height], 2, 10)
        pygame.draw.rect(screen, white, [rect_x_p2, rect_y_p2, rect_width, rect_height], 0, 10)
        # 书写文字/绘制
        pygame.display.update()  # 刷新界面

    blink = False
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False
        # 退出事件检测

        pressed = pygame.key.get_pressed()
        if catch:
            text1 = font.render("Winner:White", True, white)
        else:
            text1 = font.render("Winner:Black", True, white)

        text2 = font.render("Press R to restart", True, white)
        text3 = font.render("Press B to back to start menu", True, white)

        if pressed[pygame.K_r]:  # 重新开始
            # os.system('start ' + __file__)
            # pygame.quit()
            game()
        if pressed[pygame.K_b]:  # 回开始界面
            start_menu()
        if blink:
            screen.fill((255, 255, 255))
        else:
            screen.fill((0, 0, 0))
        blink = not blink
        screen.blit(text1, (450, 300))
        screen.blit(text2, (450, 400))
        screen.blit(text3, (450, 500))
        pygame.display.update()

start_menu()
