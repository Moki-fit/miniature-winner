#以下代码以及注释都是崔崔手搓而成 制作不易请勿随意转发
import pygame
import random
import math

# 初始化 Pygame
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("♥崔崔♥")

# 颜色定义
BLACK = (0, 0, 0)
PINK = (229, 114, 210)

# 粒子参数
particle_count = 800  # 粒子数量
particle_duration = 4  # 粒子持续时间（秒）
particle_velocity = 100
particle_size = 5
particles = []

# 计算心形路径上的点
def point_on_heart(t):
    x = 160 * math.pow(math.sin(t), 3)
    y = 130 * math.cos(t) - 50 * math.cos(2 * t) - 20 * math.cos(3 * t) - 10 * math.cos(4 * t) + 25
    return x, y

# 粒子类定义
class Particle:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.age = 0

    def update(self, delta_time):
        self.x += self.dx * delta_time
        self.y += self.dy * delta_time
        self.age += delta_time

# 初始化粒子
def create_particles():
    for _ in range(particle_count):
        t = random.uniform(-math.pi, math.pi)
        px, py = point_on_heart(t)
        px += width / 2
        py = height / 2 - py
        velocity = random.uniform(particle_velocity * 0.5, particle_velocity)
        angle = random.uniform(0, 2 * math.pi)
        dx = velocity * math.cos(angle)
        dy = velocity * math.sin(angle)
        particles.append(Particle(px, py, dx, dy))

# 主循环
running = True
create_particles()
clock = pygame.time.Clock()

while running:
    delta_time = clock.tick(60) / 1000.0  # 控制帧率，转换为秒
    screen.fill(BLACK)

    # 渲染粒子
    for particle in particles[:]:  # 使用切片以避免在遍历时修改列表
        particle.update(delta_time)
        age_ratio = particle.age / particle_duration
        if age_ratio < 1:
            size = particle_size * (1 - age_ratio)
            pygame.draw.circle(screen, PINK, (int(particle.x), int(particle.y)), int(size))
        else:
            particles.remove(particle)  # 移除超出寿命的粒子

    # 计算文本的透明度
    if particles:
        # 取最后一个粒子的年龄，计算其透明度
        last_particle = particles[-1]
        last_age_ratio = last_particle.age / particle_duration
        text_alpha = int((1 - last_age_ratio) * 255)  # 根据粒子的消失进度设置文本透明度
    else:
        text_alpha = 0  # 如果没有粒子，则完全透明

    # 显示文本
    font = pygame.font.SysFont(None, 50)  # 使用默认字体
    text = font.render("cuicui", True, PINK)  # 这里的文本可以自行修改 目前只支持英文
    text.set_alpha(text_alpha)  # 设置文本的透明度
    text_rect = text.get_rect(center=(width / 2, height / 2))
    screen.blit(text, text_rect)

    # 刷新显示
    pygame.display.flip()

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
