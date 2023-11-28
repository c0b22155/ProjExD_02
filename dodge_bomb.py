import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900


delta = {  # 練習３：押下キーと移動量の辞書
    pg.K_UP: (0, -5),  # キー：移動量／値：（横方向移動量，縦方向移動量）
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_img = pg.image.load("ex02/fig/3.png")
    kk_img = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_rct = kk_img.get_rect()  # 練習３：こうかとんSurfaceのRectを抽出する
    kk_rct.center = 900, 400  # 練習３：こうかとんの初期座標
    bb_img = pg.Surface((20, 20))   #練習１:透明のSurfaceを作る
    bb_img.set_colorkey((0, 0, 0))  #練習１：黒い部分を透明に
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  #練習１:赤い半径10の円を書く
    bb_rct = bb_img.get_rect()  #練習２：爆弾SurfaceのRentを抽出する
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 練習２：爆弾の速度

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:  #×ボタンを押すと..
                return
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:  # キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        screen.blit(bg_img, [0, 0])
        screen.blit(bb_img, bb_rct)
        kk_rct.move_ip(sum_mv[0], sum_mv[1])
        screen.blit(kk_img, kk_rct)  # 練習３：こうかとんを移動させる
        bb_rct.move_ip(vx, vy)  # 練習２：爆弾を移動させる
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__" :
    pg.init()
    main()
    pg.quit()
    sys.exit()