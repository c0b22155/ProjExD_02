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

def check_bound(rct):
    """
    オブジェクトが画面内or画面外を判定し，真理値タプルを返す関数
    引数 rct：こうかとんor爆弾SurfaceのRect
    戻り値：横方向，縦方向はみ出し判定結果（画面内：True／画面外：False）
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向はみ出し判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向はみ出し判定
        tate = False
    return yoko, tate

def idou():
    """
    移動の合計値をsum_mvに返す。キー入力した方向にこうかとんの画像が切り替わる。
    """
    kk_img0 = pg.transform.rotozoom(pg.image.load("ex02/fig/3.png"), 0, 2.0)
    kk_img = pg.transform.flip(kk_img0, True, False)  #追加機能1：飛ぶ方向に従ってこうかとん画像を切り替える
    return{  
    (0, 0):kk_img,  
    (0, +5):pg.transform.rotozoom(kk_img, -90, 1.0),
    (+5, 0):kk_img, 
    (-5, 0):kk_img0,
    (0, -5):pg.transform.rotozoom(kk_img, 90, 1.0),
    (+5, -5):pg.transform.rotozoom(kk_img, 45, 1.0),
    (-5, +5):pg.transform.rotozoom(kk_img0,45, 1.0),
    (-5, -5):pg.transform.rotozoom(kk_img0, -45, 1.0),
    (+5, +5):pg.transform.rotozoom(kk_img, -45, 1.0),
}

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("ex02/fig/pg_bg.jpg")
    kk_imgs = idou()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()  # 練習３：こうかとんSurfaceのRectを抽出する
    kk_rct.center = 900, 400  # 練習３：こうかとんの初期座標
    bb_img = pg.Surface((20, 20))   #練習１:透明のSurfaceを作る
    bb_img.set_colorkey((0, 0, 0))  #練習１：黒い部分を透明に
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  #練習１:赤い半径10の円を書く
    bb_rct = bb_img.get_rect()  #練習２：爆弾SurfaceのRentを抽出する
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    saccs = [a for a in range(1, 11)]  # 追加機能2:加速度のリスト
    c_acc = 0  # 追加機能2:現在の加速度
    vx, vy = +5, +5  # 練習２：爆弾の速度
    clock = pg.time.Clock()
    tmr = 0
    
    for r in range(1, 11):
        bb_img.set_colorkey((0, 0, 0))  # 黒い部分を透明に
    while True:
        if tmr % 100 == 0 and c_acc < len(saccs): # 追加機能2:爆弾を加速させる
           acceleration = saccs[c_acc]
           vx *= acceleration
           vy *= acceleration
           c_acc += 1      

        screen.blit(bb_img, bb_rct)
        
        for event in pg.event.get():
            if event.type == pg.QUIT:  #×ボタンを押すと..
                return
            
        if kk_rct.colliderect(bb_rct):
            print("Game Over")
            return
            
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, tpl in delta.items():
            if key_lst[k]:  # キーが押されたら
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
                
        screen.blit(bg_img, [0, 0])    
            
        kk_rct.move_ip(sum_mv[0], sum_mv[1]) #  追加機能1
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        kk_img = kk_imgs[tuple(sum_mv)]
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 練習２：爆弾を移動させる
        
        sum_mv = [0, 0]
        
        for k, tpl in delta.items():
            if key_lst[k]:  
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横方向にはみ出たら
            vx *= -1
        if not tate:  # 縦方向にはみ出たら
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)

if __name__ == "__main__" :
    pg.init()
    main()
    pg.quit()
    sys.exit()