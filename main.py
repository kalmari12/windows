import threading
import pygame
import pygame_gui

###BACKGROUND SHI###
pygame.init()

pygame.display.set_caption('Windows')
window_surface = pygame.display.set_mode((800, 600))

### Háttérszín és inicializálás
background = pygame.Surface((800, 600))
background.fill(pygame.Color("#27303B"))

### Alap változók a játékhoz mint pl.: clicks
manager = pygame_gui.UIManager((800, 600))
clicks = 0
rect = pygame.Rect(100, 100, 300, 200)

###---Gens
Gen_amount = 0
Gen_price = 0
Gen_amount_of_add = 0

###---Power
Power = 1
Power_Upgrade_Price = 0

### Clicker rész ikonjának a kreálása
Clicker_Icon = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(50, 50,70,50),
    text="Clicker",
    manager=manager,
)
### Shop ikonjának a kreálása
Shop_Icon = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(150, 50,70,50),
    text="Shop",
    manager=manager,
)

### Emiatt nem mutat semmit alapbol a kis windowwal kapcsolatban
###--- Gen adatok
my_window = None
Clicks_text = None
ggonb = None
Gen_amount_of_add_text = None

###--- Shop adatok
Shop_window = None

clock = pygame.time.Clock()
is_running = True

#########
###FUGGVENYEK###

###---CLicker ablak megnyitasa, clicker ablakon beluli dolgok csak itt lesznek tenylegesen megnyitva
def open_clicker_window():
    global my_window, Clicks_text, ggonb, Gen_amount_of_add_text

    my_window = pygame_gui.elements.UIWindow(
    rect=rect,
    manager=manager,
    window_display_title="Clicker",
    object_id='#Click_Window'
    )

    ggonb = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(0,0,150,30),
        text="Click me",
        manager=manager,
        container=my_window,
        anchors={"center":"center"}
    )

    Clicks_text = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(0,-50,100,50),
        text=f"Clicks: {clicks}",
        manager=manager,
        container=my_window,
        anchors={"center":"center"}
        )
    
    Gen_amount_of_add_text = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(0,50,100,50),
        text=f"Gen: {Gen_amount_of_add}/s",
        manager=manager,
        container=my_window,
        anchors={"center":"center"}
    )

###-- Shop ablak
shop_window_rect = pygame.Rect(100, 100,300,200)


Shop_window = pygame_gui.elements.UIWindow(
    rect=shop_window_rect,
    manager=manager,
    window_display_title="Shop",
    object_id="Shop_Window"
)

#########
###MAIN###
while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
        ### Ablak bezárása
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == my_window:
                my_window = None
        ### Ablak nyitása
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == Clicker_Icon:
                if my_window is None:
                    open_clicker_window()
                    Shop_window.show()
        ### Clickek regisztralasa es tarolasa
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == ggonb:
                clicks += 1
                print(clicks)
                Clicks_text.set_text(f"Clicks: {clicks}")


        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()