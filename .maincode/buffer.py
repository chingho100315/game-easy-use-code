imoort pygame
import sys

def Buffers(x, c, w, h, s=False):
    a = pygame.Surface((w, h))
    fps = 1

    if s:
        a.fill((0, 255, 0))
        a.blit(x, (0, 0))
        a = pygame.transform.scale(a, (w * fps, h * fps))
        a = a.convert()
        a = pygame.transform.scale(a, (w, h))
        a = a.convert()
        a.set_colorkey((0, 255, 0))
    else:
        a.fill(c)
        a.blit(x, (0, 0))
        a = pygame.transform.scale(a, (w * fps, h * fps))
        a = a.convert()
        a = pygame.transform.scale(a, (w, h))
        a = a.convert()
        a.set_colorkey(c)

    return a
