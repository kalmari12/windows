###################################
#   Comment structure: 
#   ### - main comment
#   ###--- - subcomment
#   ###--->>> - sub-subcomment
#   ###--->>>××× sub-sub-subcomment
###################################
###IMPORTS###
import threading
import pygame
import pygame_gui
#########
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
#########

### Alap változók a játékhoz mint pl.: clicks ###

clicks = 0


###---Gens
Gen_amount = 0
Gen_amount_of_add = 0

Gen_1_price = 25
Gen_2_price = 75
Gen_3_price = 225
Gen_4_price = 675

Gen_1_add_cpc = 1
Gen_2_add_cpc = 5
Gen_3_add_cpc = 50
Gen_4_add_cpc = 75

###---Power
Power = 1

###--->>> Power árak
Power_Upgrade_Price_1 = 10
Power_Upgrade_Price_2 = 30
Power_Upgrade_Price_3 = 90
Power_Upgrade_Price_4 = 180
Power_Upgrade_Price_5 = 360
Power_Upgrade_Price_6 = 620
Power_Upgrade_Price_7 = 1240

###--->>> Power Upgrade mennyisegek
Power_Upgrade_1 = 1
Power_Upgrade_2 = 5
Power_Upgrade_3 = 10
Power_Upgrade_4 = 25
Power_Upgrade_5 = 50
Power_Upgrade_6 = 150
Power_Upgrade_7 = 300
#########

###ICONS###
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
#########

### Emiatt nem mutat semmit alapbol a kis windowwal kapcsolatban ###
###--- Gen adatok
rect = pygame.Rect(100, 100, 300, 200)
my_window = None
Clicks_text = None
ggonb = None
Gen_amount_of_add_text = None
Click_Power_amount_text = None

###--->>> Gen buttons
Gen_button_1 = None
Gen_button_2 = None
Gen_button_3 = None
Gen_button_4 = None
Gen_button_5 = None
Gen_button_6 = None
Gen_button_7 = None

###--- Shop adatok
shop_window_rect = pygame.Rect(100, 100,300,200)
Shop_window = None

###--->>> Upgrade buttons
upgrade_1_button = None
upgrade_2_button = None
upgrade_3_button = None
upgrade_4_button = None
upgrade_5_button = None
upgrade_6_button = None
upgrade_7_button = None
###--->>>××× EVENT timerek upgrade
UPGRADE_TIMER_EVENT = pygame.event.custom_type()
UPGRADE_TIMER_EVENT_2 = pygame.event.custom_type()
UPGRADE_TIMER_EVENT_3 = pygame.event.custom_type()
UPGRADE_TIMER_EVENT_4 = pygame.event.custom_type()
UPGRADE_TIMER_EVENT_5 = pygame.event.custom_type()
UPGRADE_TIMER_EVENT_6 = pygame.event.custom_type()
UPGRADE_TIMER_EVENT_7 = pygame.event.custom_type()

###--->>>××× EVENT timerek gen
GEN_TICK_EVENT = pygame.event.custom_type()
GEN_TIMER_EVENT_1 = pygame.event.custom_type()



clock = pygame.time.Clock()
is_running = True

#########

###FUGGVENYEK###
###--- CLicker ablak megnyitasa, clicker ablakon beluli dolgok csak itt lesznek tenylegesen megnyitva
def open_clicker_window():
    global my_window, Clicks_text, ggonb, Gen_amount_of_add_text, Click_Power_amount_text

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
        relative_rect=pygame.Rect(0,-50,70,50),
        text=f"Clicks: {clicks}",
        manager=manager,
        container=my_window,
        anchors={"center":"center"}
    )

    Click_Power_amount_text = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(0,30,-1,-1),
        text=f"Click Power: {Power}",
        manager=manager,
        container=my_window,
        anchors={"center":"center"},
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
    global Shop_window, shop_scrolling_container, upgrades_label, upgrade_1_button, upgrade_2_button, upgrade_3_button, upgrade_4_button, upgrade_5_button, upgrade_6_button, upgrade_7_button, Gens_lable, Gen_button_1, Gen_button_2, Gen_button_3,Gen_button_4,Gen_button_5,Gen_button_6,Gen_button_7

    Shop_window = pygame_gui.elements.UIWindow(
        rect=shop_window_rect,
        manager=manager,
        window_display_title="Shop",
        object_id="Shop_Window"
    )

    shop_scrolling_container = pygame_gui.elements.UIScrollingContainer(
        relative_rect=pygame.Rect(5,5,290,220),
        manager=manager,
        starting_height=1,
        container=Shop_window,
        object_id="Shop_scroll_bar"
    )

    shop_scrolling_container.set_scrollable_area_dimensions((270, 700))

    upgrades_label = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect(0,10,131,35),
        html_text="<b>Power upgrades</b>",
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

    upgrade_2_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0,105,150,35),
    text=f"Upgrade 2 ({Power_Upgrade_Price_2}$)",
    manager=manager,
    container=shop_scrolling_container,
    tool_tip_text=f"This upgrade adds {Power_Upgrade_2} to your clicking power!",
    anchors={"centerx":"centerx",
             "top":'top',}
    )

    upgrade_3_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0,150,150,35),
    text=f"Upgrade 3 ({Power_Upgrade_Price_3}$)",
    manager=manager,
    container=shop_scrolling_container,
    tool_tip_text=f"This upgrade adds {Power_Upgrade_3} to your clicking power!",
    anchors={"centerx":"centerx",
             "top":'top',}
    )

    upgrade_4_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0,195,150,35),
    text=f"Upgrade 4 ({Power_Upgrade_Price_4}$)",
    manager=manager,
    container=shop_scrolling_container,
    tool_tip_text=f"This upgrade adds {Power_Upgrade_4} to your clicking power!",
    anchors={"centerx":"centerx",
             "top":'top',}
    )

    upgrade_5_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0,240,150,35),
    text=f"Upgrade 5 ({Power_Upgrade_Price_5}$)",
    manager=manager,
    container=shop_scrolling_container,
    tool_tip_text=f"This upgrade adds {Power_Upgrade_5} to your clicking power!",
    anchors={"centerx":"centerx",
             "top":'top',}
    )

    upgrade_6_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0,285,150,35),
    text=f"Upgrade 6 ({Power_Upgrade_Price_6}$)",
    manager=manager,
    container=shop_scrolling_container,
    tool_tip_text=f"This upgrade adds {Power_Upgrade_6} to your clicking power!",
    anchors={"centerx":"centerx",
             "top":'top',}
    )

    upgrade_7_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0,330,150,35),
    text=f"Upgrade 7 ({Power_Upgrade_Price_7}$)",
    manager=manager,
    container=shop_scrolling_container,
    tool_tip_text=f"This upgrade adds {Power_Upgrade_7} to your clicking power!",
    anchors={"centerx":"centerx",
             "top":'top',}
    )

    Gens_lable = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect(0, 380, 159,35),
        html_text="<b>Generator Upgrades</b>",
        manager=manager,
        container=shop_scrolling_container,
        anchors={"centerx":"centerx"}
    )

    Gen_button_1 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0,425,150,35),
    text=f"Gen 1 ({Gen_1_price}$)",
    manager=manager,
    container=shop_scrolling_container,
    tool_tip_text=f"This Item generates you {Gen_1_add_cpc} clicks/s!",
    anchors={"centerx":"centerx",
             "top":'top',}
    ) 

    Gen_button_2 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0,425,150,35),
    text=f"Gen 2 ({Gen_2_price}$)",
    manager=manager,
    container=shop_scrolling_container,
    tool_tip_text=f"This Item generates you {Gen_2_add_cpc} clicks/s!",
    anchors={"centerx":"centerx",
             "top":'top',}
    ) 

    Gen_button_3 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0,425,150,35),
    text=f"Gen 3 ({Gen_3_price}$)",
    manager=manager,
    container=shop_scrolling_container,
    tool_tip_text=f"This Item generates you {Gen_3_add_cpc} clicks/s!",
    anchors={"centerx":"centerx",
             "top":'top',}
    ) 

    Gen_button_4 = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(0,425,150,35),
    text=f"Gen 4 ({Gen_4_price}$)",
    manager=manager,
    container=shop_scrolling_container,
    tool_tip_text=f"This Item generates you {Gen_4_add_cpc} clicks/s!",
    anchors={"centerx":"centerx",
             "top":'top',}
    ) 
###--- power defek
def Click_add_upgraded_power(which_upgrade_button, which_upgrade_price, which_upgrade_, which_upgrade_timer_event):
    global Shop_window, shop_scrolling_container, upgrades_label, upgrade_1_button, upgrade_2_button, upgrade_3_button, upgrade_4_button, upgrade_5_button, upgrade_6_button, upgrade_7_button, Gens_lable, clicks
    if clicks >= which_upgrade_price:
        clicks -= which_upgrade_price
        Power_Upgrade(which_upgrade_)
        Clicks_text.set_text(f"Clicks: {clicks}")
        Clicks_text.set_dimensions((-1, -1))                  
    else:
        which_upgrade_button.set_text("Not enough clicks!")
        pygame.time.set_timer(which_upgrade_timer_event, 2000)

def Power_Upgrade(which_upgrade):
    global Power, Click_Power_amount_text
    Power += which_upgrade
    Click_Power_amount_text.set_text(f"Click Power: {Power}")
    return Power 

def Gen_Upgrade(which_gen_price, which_cpc, which_gen_button, which_ggen_timer_event):
    global power, Gen_amount_of_add_text, Gen_amount_of_add, clicks, Gen_button_1, Gen_button_2, Gen_button_3, Gen_button_4, Gen_button_5, Gen_button_6, Gen_button_7
    if clicks >= which_gen_price:
        clicks -= which_gen_price
        Gen_amount_of_add += which_cpc
        clicks += Gen_amount_of_add
        Gen_amount_of_add_text.set_text(f"Gen: {Gen_amount_of_add}/s")
        Gen_amount_of_add_text.set_dimensions((-1, -1))
    else:
        which_gen_button.set_text("Not enough clicks!")
        pygame.time.set_timer(which_ggen_timer_event, 2000)
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
###POWER_UPGRADES###
        ### Upgrade_1 power hozzaadas
        if upgrade_1_button is not None and event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == upgrade_1_button:
                Click_add_upgraded_power(upgrade_1_button,Power_Upgrade_Price_1,Power_Upgrade_1,UPGRADE_TIMER_EVENT)
        ###--->>> visszaallitja a gombot "Not enough clicks!"-ről az eredeti szövegre
        if event.type == UPGRADE_TIMER_EVENT:
            if upgrade_1_button is not None:
                upgrade_1_button.set_text(f"Upgrade 1 ({Power_Upgrade_Price_1}$)")
            pygame.time.set_timer(UPGRADE_TIMER_EVENT, 0)

        ### upgrade_2 power hozzadasa
        if upgrade_2_button is not None and event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == upgrade_2_button:
                Click_add_upgraded_power(upgrade_2_button,Power_Upgrade_Price_2,Power_Upgrade_2,UPGRADE_TIMER_EVENT_2)
        if event.type == UPGRADE_TIMER_EVENT_2:
            if upgrade_2_button is not None:
                upgrade_2_button.set_text(f"Upgrade 2 ({Power_Upgrade_Price_2}$)")
            pygame.time.set_timer(UPGRADE_TIMER_EVENT_2, 0)

        ### upgrade_3 power hozzadasa
        if upgrade_3_button is not None and event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == upgrade_3_button:
                Click_add_upgraded_power(upgrade_3_button,Power_Upgrade_Price_3,Power_Upgrade_3,UPGRADE_TIMER_EVENT_3)
        if event.type == UPGRADE_TIMER_EVENT_3:
            if upgrade_3_button is not None:
                upgrade_3_button.set_text(f"Upgrade 3 ({Power_Upgrade_Price_3}$)")
            pygame.time.set_timer(UPGRADE_TIMER_EVENT_3, 0)    
        ### upgrade_4 power hozzadasa
        if upgrade_4_button is not None and event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == upgrade_4_button:
                Click_add_upgraded_power(upgrade_4_button,Power_Upgrade_Price_4,Power_Upgrade_4,UPGRADE_TIMER_EVENT_4)
        if event.type == UPGRADE_TIMER_EVENT_4:
            if upgrade_4_button is not None:
                upgrade_4_button.set_text(f"Upgrade 4 ({Power_Upgrade_Price_4}$)")
            pygame.time.set_timer(UPGRADE_TIMER_EVENT_4, 0)

        ### upgrade_5 power hozzadasa
        if upgrade_5_button is not None and event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == upgrade_5_button:
                Click_add_upgraded_power(upgrade_5_button,Power_Upgrade_Price_5,Power_Upgrade_5,UPGRADE_TIMER_EVENT_5)
        if event.type == UPGRADE_TIMER_EVENT_5:
            if upgrade_5_button is not None:
                upgrade_5_button.set_text(f"Upgrade 5 ({Power_Upgrade_Price_5}$)")
            pygame.time.set_timer(UPGRADE_TIMER_EVENT_5, 0)

        ### upgrade_6 power hozzadasa
        if upgrade_6_button is not None and event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == upgrade_6_button:
                Click_add_upgraded_power(upgrade_6_button,Power_Upgrade_Price_6,Power_Upgrade_6,UPGRADE_TIMER_EVENT_6)
        if event.type == UPGRADE_TIMER_EVENT_6:
            if upgrade_6_button is not None:
                upgrade_6_button.set_text(f"Upgrade 6 ({Power_Upgrade_Price_6}$)")
            pygame.time.set_timer(UPGRADE_TIMER_EVENT_6, 0)

        ### upgrade_7 power hozzadasa
        if upgrade_7_button is not None and event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == upgrade_7_button:
                Click_add_upgraded_power(upgrade_7_button,Power_Upgrade_Price_7,Power_Upgrade_7,UPGRADE_TIMER_EVENT_7)
        if event.type == UPGRADE_TIMER_EVENT_7:
            if upgrade_7_button is not None:
                upgrade_7_button.set_text(f"Upgrade 7 ({Power_Upgrade_Price_7}$)")
            pygame.time.set_timer(UPGRADE_TIMER_EVENT_7, 0)

##############################################################################################################################
###GENS###
        if event.type == pygame_gui.UI_BUTTON_PRESSED and Gen_button_1 is not None:
            if event.ui_element == Gen_button_1:
                
##############################################################################################################################
    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
#########