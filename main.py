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
manager = pygame_gui.UIManager((800, 600))
manager.preload_fonts([
    {
        'name': 'noto_sans',
        'point_size': 14,
        'style': 'bold'
    }
])

### Alap változók a játékhoz mint pl.: clicks

clicks = 0


###---Gens
Gen_amount = 0
Gen_price = 0
Gen_amount_of_add = 0

###---Power
Power = 1

###--->>> Power árak
Power_Upgrade_Price_1 = 10
Power_Upgrade_Price_2 = 30
Power_Upgrade_Price_3 = 75
Power_Upgrade_Price_4 = 125

###--->>> Power Upgrade mennyisegek
Power_Upgrade_1 = 1
Power_Upgrade_2 = 5
Power_Upgrade_3 = 10
Power_Upgrade_4 = 20

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
rect = pygame.Rect(100, 100, 300, 200)
my_window = None
Clicks_text = None
ggonb = None
Gen_amount_of_add_text = None

###--- Shop adatok
shop_window_rect = pygame.Rect(100, 100,300,200)
Shop_window = None

###--->>> Upgrade 1 button
upgrade_1_button = None
UPGRADE_TIMER_EVENT = pygame.event.custom_type()

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
def open_shop_window():
    global Shop_window, shop_scrolling_container, upgrades_label, upgrade_1_button  

    Shop_window = pygame_gui.elements.UIWindow(
        rect=shop_window_rect,
        manager=manager,
        window_display_title="Shop",
        object_id="Shop_Window"
    )

    shop_scrolling_container = pygame_gui.elements.UIScrollingContainer(
        relative_rect=pygame.Rect(5,5,290,160),
        manager=manager,
        starting_height=1,
        container=Shop_window,
        object_id="Shop_scroll_bar"
    )

    shop_scrolling_container.set_scrollable_area_dimensions((270, 400))

    upgrades_label = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect(0,10,85,35),
        html_text="<b>Upgrades</b>",
        manager=manager,
        container=shop_scrolling_container,
        anchors={"centerx":"centerx",
                 "top":"top"}
    )   

    upgrade_1_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect(0,60,150,35),
        text=f"Upgrade 1 ({Power_Upgrade_Price_1}$)",
        manager=manager,
        container=shop_scrolling_container,
        tool_tip_text=f"This upgrade adds {Power_Upgrade_1} to your clicking power!",
        anchors={"centerx":"centerx",
                 "top":'top',}
    )

###--- power defek
def Power_Upgrade(which_upgrade):
    global Power
    Power += which_upgrade
    return Power
#########
###MAIN###
while is_running:
    time_delta = clock.tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        ### Clicker Ablak bezárása
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == my_window:
                my_window = None
        ### Clicker Ablak nyitása
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == Clicker_Icon:
                if my_window is None:
                    open_clicker_window()
        ### Clickek regisztralasa es tarolasa
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == ggonb:
                clicks += Power
                print(clicks)
                Clicks_text.set_text(f"Clicks: {clicks}")
        ### Shop window nyitása
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == Shop_Icon:
                if Shop_window is None:
                    open_shop_window()
        ### Shop window bezarasa
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            if event.ui_element == Shop_window:
                Shop_window = None
        manager.process_events(event)
        ### Upgrade_1 power hozzaadas
        if upgrade_1_button is not None and event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == upgrade_1_button:
                if clicks >= Power_Upgrade_Price_1:
                    clicks -= Power_Upgrade_Price_1
                    Power_Upgrade(Power_Upgrade_1)
                else:
                    upgrade_1_button.set_text("Not enough clicks!")
                    pygame.time.set_timer(UPGRADE_TIMER_EVENT, 2000)
        if event.type == UPGRADE_TIMER_EVENT:
            if upgrade_1_button is not None:
                upgrade_1_button.set_text(f"Upgrade 1 ({Power_Upgrade_Price_1}$)")
            pygame.time.set_timer(UPGRADE_TIMER_EVENT, 0)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()