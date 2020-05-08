let app = new PIXI.Application({
        width: 800,
        height: 800,
        antialias: true,
        transparent: true,
        resolution: 1,
        sharedTicker: true,
        backgroundColor:0xfe4949,
    }
);

document.body.appendChild(app.view);


PIXI.loader

    .add("/static/lettergame/image/buntemplate.png")
    .add("/static/lettergame/image/bottombuntemplate.png")
    .add("/static/lettergame/image/bunstationlabel.png")
    .add("/static/lettergame/image/meatstationlabel.png")
    .add("/static/lettergame/image/addonslabel.png")
    .add("/static/lettergame/image/meattemplate.png")
    .add("/static/lettergame/image/servelabel.png")
    .add("/static/lettergame/image/tjoiner.png")
    .add("/static/lettergame/image/hjoiner.png")
    .add("/static/lettergame/image/finale.png")
    .add("/static/lettergame/image/neutralguy.png")
    .add("/static/lettergame/image/sadguy.png")
    .add("/static/lettergame/image/happyguy.png")
    .add("/static/lettergame/image/recipetemplate.png")
    .add("/static/lettergame/image/burgergametitle.png")
    .add("/static/lettergame/image/start.png")
    .add("/static/lettergame/image/instructions.png")
    .add("/static/lettergame/image/go.png")
    .add("/static/lettergame/image/background.png")
    .add("/static/lettergame/image/levelonelabel.png")
    .add("/static/lettergame/image/leveltwolabel.png")
    .add("/static/lettergame/image/levelthreelabel.png")
    .add("/static/lettergame/image/nowloading.png")
    .add("/static/lettergame/image/speechbubble.png")
    .add("/static/lettergame/image/check.png")
    .add("/static/lettergame/image/numberone.png")
    .add("/static/lettergame/image/numbertwo.png")
    .add("/static/lettergame/image/numberthree.png")
    .add("/static/lettergame/image/numberfour.png")
    .add("/static/lettergame/image/numberfive.png")
    .add("/static/lettergame/image/numbersix.png")
    .add("/static/lettergame/image/numberseven.png")
    .add("/static/lettergame/image/numbereight.png")
    .add("/static/lettergame/image/numbernine.png")
    .add("/static/lettergame/image/numberzero.png")
    .add("/static/lettergame/image/burgersmade.png")
    .add("/static/lettergame/image/stats.png")
    .add("/static/lettergame/image/goback.png")
    .add("/static/lettergame/image/x.png")
    .add("/static/lettergame/image/quit_button.png")
    .load(main);

function main(){
    startup();
}

function startup() {

    upScroll = "off";

    let title = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/burgergametitle.png"].texture);
    title.y = -50;
    title.x = 100;

    let start = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/start.png"].texture);
    start.interactive = true;
    start.y = 800;
    start.x = 220;
    start.height = 151;
    start.width = 370;
    start.on("mousedown", scrollOn);

    let instructions = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/instructions.png"].texture);
    instructions.x = 50;
    instructions.y = 1000;

    let go = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/go.png"].texture);
    go.x = 285;
    go.y = 1710;
    go.interactive = true;
    go.on("mousedown", goTo);

    const startup_container = new PIXI.Container();
    app.stage.addChild(startup_container);
    startup_container.addChild(title);
    startup_container.addChild(start);
    startup_container.addChild(instructions);
    startup_container.addChild(go);

    function gameLoop() {
        requestAnimationFrame(gameLoop);
        if (title.y <= 130 && upScroll == "off") {
            title.y += 5;
            start.y -= 5;
        }
    }

    gameLoop();

    function scrollOn() {
        upScroll = "on";
        scroll()
    }

    function scroll() {
        requestAnimationFrame(scroll);
        if (upScroll == "on" && instructions.y >= 20) {
            title.y -= 7;
            start.y -= 7;
            instructions.y -= 7;
            go.y -= 7;
        }
    }

    function goTo() {
        app.stage.removeChild(startup_container);
        level_setup();
    }
}




//function level_selection_screen() {
//    let levelonelabel = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/levelonelabel.png"].texture);
//    levelonelabel.interactive = true;
//    levelonelabel.y = 110;
//    levelonelabel.x = 37;
//
//    let leveltwolabel = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/leveltwolabel.png"].texture);
//    leveltwolabel.interactive = true;
//    leveltwolabel.y = 345;
//    leveltwolabel.x = 37;
//
//    let levelthreelabel = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/levelthreelabel.png"].texture);
//    levelthreelabel.interactive = true;
//    levelthreelabel.y = 585;
//    levelthreelabel.x = 37;
//
//    const level_select_container = new PIXI.Container();
//    app.stage.addChild(level_select_container);
//    level_select_container.addChild(levelonelabel,leveltwolabel, levelthreelabel);
//
//    levelonelabel.on("mousedown", function(){ level = "easy"; level_set();});
//    leveltwolabel.on("mousedown",  function(){ level = "medium"; level_set();});
//    levelthreelabel.on("mousedown",  function(){ level = "hard"; level_set();});
//
//    function level_set(){
//        console.log(level);
//        let difficulty_times = {
//            "easy": 50000,
//            "medium":50000,
//            "hard": 50000,
//        }
//        timeUntilEnd = difficulty_times[level];
//        app.stage.removeChild(level_select_container);
//        level_setup()
//    }
//}

let level = "easy"
let timeUntilEnd = 500000;
let correct_responses = 0;
let incorrect_responses = 0;

function level_setup() {
    // 0. set the level time


    // 0. set the level difficulty
    var urlParams = new URLSearchParams(window.location.search);
    level = urlParams.get('level');
    timeUntilEnd = urlParams.get('time_limit');

    // TODO: BEGIN LEVEL SESSION

    // 1. Load in the static assets:
    const bg_container = new PIXI.Container(name = "background");
    app.stage.addChild(bg_container);
    bg_setup(bg_container);
    const station_buttons_container = new PIXI.Container();
    station_buttons_container.name = "station_buttons"
    button_setup(station_buttons_container);
    app.stage.addChild(station_buttons_container);
    quit_button_setup("end_screen");

    // 2. Prepare Bun section frontend
    const bun_container = new PIXI.Container();
    bun_container.name = 'bun';
    const tb_container = new PIXI.Container();
    const bb_container = new PIXI.Container();
    bun_container.width = app.screen.width * (1 / 4);
    bb_container.width = app.screen.width * (1 / 4);
    tb_container.name = 'prefix'
    tb_container.height = app.screen.height * (1 / 6);
    bb_container.height = app.screen.height * (1 / 6);
    bb_container.name='suffix';
    bun_container.width = app.screen.width;


    bun_section_setup(tb_container, bb_container);
    bun_container.addChild(tb_container, bb_container);
    bun_container.visible = true;
    app.stage.addChild(bun_container);

    // 3, Prepare Burger section frontend
    const burger_container = new PIXI.Container();
    burger_container.width = app.screen.width * (1 / 2);
    burger_container.height = app.screen.height * (1 / 6);




    burger_section_setup(burger_container);
    burger_container.visible = false;
    burger_container.name="verb";
    app.stage.addChild(burger_container);


    // 4. Prepare Toppings section frontend
    const addon_container = new PIXI.Container();
    addon_container.width = app.screen.width * (1 / 3);
    addon_container.height = app.screen.height * (1 / 6);


    addon_section_setup(addon_container);
    addon_container.visible = false;
    addon_container.name = "joiner";
    app.stage.addChild(addon_container);

    // 6. recipe building backend
    const tray_container = new PIXI.Container();
    tray_container.name = "tray";
    tray_container.width = app.screen.width;
    tray_container.height = app.screen.height * (1 / 4);
    tray_setup(tray_container);
    app.stage.addChild(tray_container);

    // 7. recipe submission backend
    const order_container = new PIXI.Container();
    order_container.name = "order";
    order_container.x = 0;
    order_container.y = app.screen.height *(2/5);
    app.stage.addChild(order_container);

    // 7.5. Order description

    let recipe_description = new PIXI.Graphics();
    recipe_description.name = "recipe_description"
    app.stage.addChild(recipe_description);
    update_description();
//    // TODO: Finish implementing clear button
//    let clear_order_button = new PIXI.Graphics();
//    clear_order_button.name = "clear_order"
//    app.stage.addChild(clear_order_button)
//    setup_clear_order();
    // Preparing feedback
    setup_feedback();


    // 8. start clock!
    game_timer_setup()
    menu_buttons = station_buttons_container.children;
    let views = {
        "burgerstation": burger_container,
        "bunstation": bun_container,
        "addonstation": addon_container,
    };
    on_click_listeners(menu_buttons,views);

}

function on_click_listeners(menu_buttons, views){
    for (i = 0; i < menu_buttons.length; i++) {
        menu_buttons[i].on("mousedown", function (button) {
            menu_buttons.map((button) => {
                if (button.name != "servestation"){
                    views[button.name].visible = false;
                    views[button.name].interactive = false;
                }
            });
            if (this.name == "servestation"){

                let conjugation_object = JSON.parse(document.getElementById("conjugation_list").textContent);
                let verb = JSON.parse(document.getElementById("verb").textContent)[0];
                let order = app.stage.getChildByName('order').children;
                // Confusing, but this ensures if the user has no addons entered, that it will mark correctly.
                let final_order = {"joiner": ""};
                let correct_components = {"joiner": conjugation_object.joiner == ""};
                order.map(child => {final_order[child.type]=child.getChildAt(0).text});
                order.map(child => {correct_components[child.type] = child.getChildAt(0).text == conjugation_object[child.type]})
                display_feedback(correct_components);
                let correct = Object.values(correct_components)
                correct = correct.reduce((total, value) => {return total && value}, true);
                if (correct){
                    correct_responses += 1;
                }
                else{
                    incorrect_responses +=1;
                }
                // get new order
                post_order_to_backend(setup_new_order);
            }
            else{
                views[this.name].visible = true;
                views[this.name].interactive = true;
                if (this.name == "bunstation") {
                    views[this.name].getChildAt(0).children.map(child => {child.x = child.x_original;
                                                                    child.y = child.y_original;});
                    views[this.name].getChildAt(1).children.map(child => {child.x = child.x_original;
                                                                    child.y = child.y_original;});
                }
                else {
                    views[this.name].children.map(child => {child.x = child.x_original;
                                                        child.y = child.y_original;});
                }
            }
        });
    }
    function setup_new_order(data) {
            let order = app.stage.getChildByName("order");
            let prefix_array = document.getElementById("prefix_distractors");
            let suffix_array = document.getElementById("suffix_distractors");
            let verb_array = document.getElementById("verb_distractors");
            let verb = document.getElementById("verb");
            let conjugation_list = document.getElementById("conjugation_list");
            // TODO: begin next question for the game
            prefix_array.textContent = JSON.stringify(data.prefix_distractors);
            suffix_array.textContent = JSON.stringify(data.suffix_distractors);
            verb_array.textContent = JSON.stringify(data.verb_distractors);
            verb.textContent = JSON.stringify(data.verb);
            conjugation_list = JSON.stringify(data.conjugation_list);
            setTimeout(hide_feedback, 3000);
            // remove all children from the menus
            views.bunstation.children.map(child => child.removeChildren());
            views.addonstation.removeChildren();
            views.burgerstation.removeChildren();
            // remove all children from the order
            app.stage.getChildByName('order').removeChildren();

            bun_section_setup(views.bunstation.getChildByName("prefix"),views.bunstation.getChildByName("suffix"));
            burger_section_setup(views.burgerstation);
            addon_section_setup(views.addonstation);
            update_description();
            reset_to_bun_station(menu_buttons);

    }
    function reset_to_bun_station(menu_buttons){
        menu_buttons.map((button) => {
            if (button.name == "bunstation"){
                views[button.name].getChildAt(0).children.map(child => {child.x = child.x_original;
                                                                    child.y = child.y_original;});
                views[button.name].getChildAt(1).children.map(child => {child.x = child.x_original;
                                                                    child.y = child.y_original;});
                views[button.name].visible = true;
                views[button.name].interactive = true;
            }
            else if (button.name != "servestation"){
                views[button.name].visible = false;
                views[button.name].interactive = false;
            }

        });
    }
}

let gameTimer = null
function game_timer_setup() {
    let countdownclock = new PIXI.Text("Time remaining: " + (timeUntilEnd / 1000).toString());
    app.stage.addChild(countdownclock);
    countdownclock.x = 500;

    gameTimer = setTimeout(function tick(clock) {
        timeUntilEnd = timeUntilEnd - 1000;
        clock.text = "Time remaining: " + (timeUntilEnd / 1000).toString()
        if (timeUntilEnd >= 1000) {
            timerId = setTimeout(tick, 1000, countdownclock);
        } else {
            end_game_setup();
        }
    }, 1000, countdownclock);

}

function bg_setup(bg_container) {
    let background = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/background.png"].texture);
    background.height = 800;
    background.width = 800;
    bg_container.addChild(background);

    let npc_guy = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/happyguy.png"].texture);
    npc_guy.x = 305;
    npc_guy.y = 130;
    npc_guy.height = 200;
    npc_guy.width = 200;
    bg_container.addChild(npc_guy);
}

function button_setup(station_buttons_container) {
    let bunstationlabel = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/bunstationlabel.png"].texture);
    let meatstationlabel = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/meatstationlabel.png"].texture);
    let addonslabel = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/addonslabel.png"].texture);
    let servelabel = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/servelabel.png"].texture);
    let resetlabel = new PIXI.Text()
    bunstationlabel.x = 10;
    bunstationlabel.y = 760;
    bunstationlabel.interactive = true;
    bunstationlabel.name = "bunstation"
    meatstationlabel.x = 210;
    meatstationlabel.y = 760;
    meatstationlabel.interactive = true;
    meatstationlabel.name = "burgerstation";
    addonslabel.x = 410;
    addonslabel.y = 760;
    addonslabel.interactive = true;
    addonslabel.name = "addonstation";
    servelabel.x = 610;
    servelabel.y = 760;
    servelabel.interactive = true;
    servelabel.name = "servestation";


    station_buttons_container.addChild(bunstationlabel, meatstationlabel, addonslabel, servelabel)
}

function bun_section_setup(tb_container, bb_container) {
    const topbun = new PIXI.Texture.from("/static/lettergame/image/buntemplate.png");
    const bottombun = new PIXI.Texture.from("/static/lettergame/image/bottombuntemplate.png");
    let topbuntext = JSON.parse(document.getElementById("prefix_distractors").textContent);
    let bottombuntext = JSON.parse(document.getElementById("suffix_distractors").textContent);
    topbuntext = [...new Set(topbuntext)];
    bottombuntext = [...new Set(bottombuntext)];
    let top_buns = [];
    for (let i = 0; i < Math.min(topbuntext.length,4); i++) {
        const bun = new PIXI.Sprite(topbun);
        bun.anchor.set(0.5, 0.5);
        bun.x = bun.x_original =  (i % 2) * 90;
        bun.y = bun.y_original = Math.floor(i / 2) * 90;
        top_buns.push(bun)

    }
    tb_container.x = app.screen.width * (1 / 4);
    tb_container.y = app.screen.height * (3.5 / 5);
    tb_container.pivot.x = tb_container.width / 2;
    tb_container.pivot.y = tb_container.height / 2;
    for (i = 0; i < top_buns.length; i++) {
        top_buns[i].type = "prefix";
        top_buns[i].buttonMode = true;
        top_buns[i].width = 82;
        top_buns[i].height = 46;
        top_buns[i].ontrayx = 350;
        top_buns[i].ontrayy = 350;
        text_child = new PIXI.Text(topbuntext[i],
            {
                fontFamily: 'Arial',
                fontSize: 14,
                fontWeight: 'bold',
                strokeThickness: 2,
                stroke: 'white',
                align: 'center'
            });
        text_child.anchor.set(.5, 0.3);
        top_buns[i].addChild(text_child);
        tb_container.addChild(top_buns[i]);
    }

    let bottom_buns = [];
    for (let i = 0; i < Math.min(bottombuntext.length,4); i++) {
        const bun = new PIXI.Sprite(bottombun);
        bun.anchor.set(0.5, 0.3);
        bun.x = bun.x_original = (i % 2) * 90;
        bun.y = bun.y_original = Math.floor(i / 2) * 90;
        bottom_buns.push(bun)
    }
    bb_container.x = app.screen.width * (3 / 4);
    bb_container.y = app.screen.height * (3.5 / 5);
    bb_container.pivot.x = bb_container.width / 2;
    bb_container.pivot.y = bb_container.height / 2;
    for (i = 0; i < bottom_buns.length; i++) {
        bottom_buns[i].type = "suffix";
        bottom_buns[i].buttonMode = true;
        bottom_buns[i].width = 84;
        bottom_buns[i].height = 30;
        bottom_buns[i].ontrayx = 350;
        bottom_buns[i].ontrayy = 424;
        text_child = new PIXI.Text(bottombuntext[i],
            {
                fontFamily: 'Arial',
                fontSize: 14,
                fontWeight: 'bold',
                strokeThickness: 2,
                stroke: 'white',
                align: 'center'
            });
        text_child.anchor.set(0.5, 0.3);
        bottom_buns[i].addChild(text_child)
        bb_container.addChild(bottom_buns[i]);
    }
    top_buns.map(create_drag_and_drop);
    bottom_buns.map(create_drag_and_drop);
    return {top_buns: top_buns, bottom_buns: bottom_buns}
}

function burger_section_setup(burger_container) {
    let burgtext = JSON.parse(document.getElementById("verb_distractors").textContent);
    const burger = new PIXI.Texture.from("/static/lettergame/image/meattemplate.png");
    // top buns
    let burgers = [];
    for (let i = 0; i < Math.min(burgtext.length,4); i++) {
        const patty = new PIXI.Sprite(burger);
        patty.anchor.set(0.5, 0.5);
        patty.x = patty.x_original = (i % 2) * 275;
        patty.y = patty.y_original = Math.floor(i / 2) * 90;
        burgers.push(patty)
    }
    burger_container.x = app.screen.width * (1 / 4);
    burger_container.y = app.screen.height * (3.5 / 5);
    burger_container.pivot.x = burger_container.width / 2;
    burger_container.pivot.y = burger_container.height / 2;
    for (i = 0; i < burgers.length; i++) {
        burgers[i].type = "verb";
        burgers[i].buttonMode = true;
        burgers[i].width = 82;
        burgers[i].height = 35;
        burgers[i].ontrayx = 350;
        burgers[i].ontrayy = 396;
        text_child = new PIXI.Text(burgtext[i],
            {
                fontFamily: 'Arial',
                fontSize: 14,
                fontWeight: 'bold',
                strokeThickness: 2,
                stroke: 'white',
                align: 'center'
            });
        text_child.anchor.set(.5, 0.6);
        burgers[i].addChild(text_child);
        burger_container.addChild(burgers[i]);
    }
    burgers.map(create_drag_and_drop);
    return burgers;
}

function addon_section_setup(addon_container) {
    // original color code is f51945
    let addontext = ["t" , "h", "e "];
    let addons = [];
    for (let i = 0; i < 3; i++) {
        let index = i;
        let texture_location = '/static/lettergame/image/addon' + i.toString() + '.png';
        const addon_texture = new PIXI.Texture.from(texture_location);
        const addon = new PIXI.Sprite(addon_texture);
        addon.anchor.set(0.5, 0.5);
        addon.x = addon.x_original = (i % 2) * 90;
        addon.y = addon.y_original = Math.floor(i / 2) * 90;
        addons.push(addon)
    }
    addon_container.x = app.screen.width * (1 / 4);
    addon_container.y = app.screen.height * (3.5 / 5);
    addon_container.pivot.x = addon_container.width / 2;
    addon_container.pivot.y = addon_container.height / 2;
    for (i = 0; i < addons.length; i++) {
        addons[i].type = "joiner";
        addons[i].buttonMode = true;
        addons[i].width = 34;
        addons[i].height = 80;
        addons[i].ontrayx = 350;
        addons[i].ontrayy = 335;
        text_child = new PIXI.Text(addontext[i],
            {
                fontFamily: 'Arial',
                fontSize: 16,
                fontWeight: 'bold',
                strokeThickness: 2,
                stroke: 'white',
                align: 'center'
            });
        text_child.anchor.set(.5, 0.6);
        addons[i].addChild(text_child);
        addon_container.addChild(addons[i]);
    }
    addons.map(create_drag_and_drop);
    return addons;
}

function get_duplicates(tar,order) {
    let existing = order.children.filter(child => child.type == tar.type);
    if (existing != []) {
        return existing[0]
    }
    return null;
}

function create_drag_and_drop(tar) {
    function onDragStart(e) {
        this.drag = true;
        this.alpha = 0.7;
        this.data = e.data;
    }

    function onDragEnd() {
        this.drag = false;


        let tray = app.stage.getChildByName('tray');
        let tray_rect = tray.getBounds();
        let abs_position = tar.getGlobalPosition();

        if (tray_rect.contains(abs_position.x,abs_position.y)){
            if (tar.parent.name != "order"){
                tar.parent.removeChild(tar);
                let order = app.stage.getChildByName("order");
                let dup_type_in_order = get_duplicates(tar,order);
                if (dup_type_in_order){
                    return_order_member_to_parent(dup_type_in_order);
                }
                order.addChild(tar);
            }
            // Set object in place inside the order
            let ordering = ['prefix','verb','suffix','joiner']
            let y_pos = [40, 80, 100]
            let index = ordering.indexOf(tar.type);
            if( index > -1 && index < 3){
                tar.x = 400;
                tar.y = y_pos[index];
            }
            else{
                tar.x = app.stage.width/2 + 125;
                tar.y = 100;
            }
        }
        else{
            if (tar.parent.name == "order"){
                return_order_member_to_parent(this);
            }
        }
        this.alpha = 1;
        this.data = null;
    }

    function onDragContinue() {
        if (this.drag) {
            let newPosition = this.data.getLocalPosition(this.parent);
            this.x = newPosition.x;
            this.y = newPosition.y;
        }
    }

    tar.drag = false;
    tar.interactive = true;
    tar.on("mousedown", onDragStart)
        .on('touchstart', onDragStart)
        .on("mouseup", onDragEnd)
        .on('mouseupoutside', onDragEnd)
        .on('touchend', onDragEnd)
        .on('touchendoutside', onDragEnd)
        .on("mousemove", onDragContinue)
        .on('touchmove', onDragContinue);
}

function return_order_member_to_parent(target) {
    let target_container = target.type;
    let originalParent = null;
    if (target_container == "suffix" || target_container == "prefix"){
        originalParent = app.stage.getChildByName('bun').getChildByName(target_container);
    }
    else{
        originalParent = app.stage.getChildByName(target_container);
    }
    originalParent.addChild(target);
    target.x = target.x_original;
    target.y = target.y_original;
}

function tray_setup(tray_container) {
    tray_container.x = 0;
    tray_container.y = app.screen.height * (2 / 5);
    tray_container.pivot.x = tray_container.width / 2;
    tray_container.pivot.y = tray_container.height / 2;
    let tray_graphic = new PIXI.Graphics();
    tray_graphic.beginFill(0x333FFFF);
    tray_graphic.drawRect(0,0, app.stage.width, app.stage.height * (1/4));
    tray_graphic.endFill();
    tray_container.alpha=0;
    tray_container.addChild(tray_graphic);
}

function post_order_to_backend(callback){

    let order = app.stage.getChildByName("order").children;
    let final_order = {"joiner": ""};
    order.map(child => {final_order[child.type]=child.getChildAt(0).text});
    let prefix_array = document.getElementById("prefix_distractors");
    let suffix_array = document.getElementById("suffix_distractors");
    let verb_array = document.getElementById("verb_distractors");
    let verb = document.getElementById("verb");
    let conjugation_list = document.getElementById("conjugation_list");

    $.ajax({
          type:'POST',
          url: "",
          data:{
          'prefix_distractors[]': JSON.parse(prefix_array.textContent),
          'suffix_distractors[]': JSON.parse(suffix_array.textContent),
          'verb_distractors[]': JSON.parse(verb_array.textContent),
          'conjugation_list[]': JSON.parse(conjugation_list.textContent),
          'correct_verb[]': JSON.parse(verb.textContent),
          'on_burger[]': order
          },
          success: callback,
          error:function(error){
            console.log(error)
            return error
          }
        });
}

function update_description(){
    let long_versions =  {
        "1S": "1st person singular",
        "2S": "2nd person singular",
        "3S": "3rd person singular",
        "2I": "2nd person inclusive",
        "1P": "1st person plural",
        "2P": "2nd person plural",
        "3P": "3rd person plural",
        "3'": "3rd person obviate",
    }
    let verb = JSON.parse(document.getElementById("verb").textContent);
    let conjugation = JSON.parse(document.getElementById("conjugation_list").textContent);

    let order_description = ""
    if (level == "easy"){
        order_description = (verb[0] + "\n\n" + long_versions[conjugation.person]);
    }
    else{
        order_description = (conjugation.translation + "\n\n\" " + verb[1] + "\"\n\n" + long_versions[conjugation.person]);
    }

    let recipe_description = app.stage.getChildByName('recipe_description');
    let existing_text = recipe_description.getChildByName('recipe_text')
    if (existing_text){
        recipe_description.alpha = 0.6
        recipe_description.beginFill(0x9c9da4);
        recipe_description.lineStyle(4, 0x000000, 1);
        recipe_description.drawRect(10, 10, existing_text.width + 40, existing_text.height + 40 );
        recipe_description.endFill();
        setTimeout(() =>{
            recipe_description.clear();
            existing_text.text = order_description;
            recipe_description.alpha = 1;
            setTimeout(() => {
                recipe_description.clear();
                recipe_description.beginFill(0xFFFFFF);
                recipe_description.lineStyle(4, 0x000000, 1);
                recipe_description.drawRect(10, 10, existing_text.width + 40, existing_text.height + 40 );
                recipe_description.endFill();
                recipe_description.addChild(existing_text);
            }, 300);

        }, 1000);
    }
    else{
        let recipe_text = new PIXI.Text(order_description,{
        wordWrap: true,
        wordWrapWidth: 100,
        fontSize: 20
        });
        recipe_text.x = 30;
        recipe_text.y = 22;
        recipe_text.name = 'recipe_text';
        existing_text = recipe_text;
        recipe_description.beginFill(0xFFFFFF);
        recipe_description.lineStyle(4, 0x000000, 1);
        recipe_description.drawRect(10, 10, existing_text.width + 40, existing_text.height + 40 );
        recipe_description.endFill();
        recipe_description.addChild(existing_text);
    }
}

function setup_feedback(){
    let answer_feedback = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/speechbubble.png"].texture);
    answer_feedback.x = 450;
    answer_feedback.y = 50;
    answer_feedback.height = 250;
    answer_feedback.width = 250;
    answer_feedback.visible=false;
    answer_feedback.name="answer_feedback";
    app.stage.addChild(answer_feedback);
    answer_components = ["prefix", "suffix", "verb", "joiner"];
    answer_components.map((component, index) =>{
        let response = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/check.png"].texture);
        response.name = component;
        response.x = 210;
        response.y = 40 + index * 50;
//        if (component == "joiner"){
//            response.x = ;
//        }
        answer_feedback.addChild(response)
    })
}

function display_feedback(correct_components){
    let answer_feedback = app.stage.getChildByName('answer_feedback');
    answer_feedback.children.map(response => {
        if (correct_components[response.name]){
            response.texture = PIXI.loader.resources["/static/lettergame/image/check.png"].texture;
        }
        else{
            response.texture = PIXI.loader.resources["/static/lettergame/image/x.png"].texture;
        }
    });
    answer_feedback.visible=true;
}

function hide_feedback(){
    let answer_feedback = app.stage.getChildByName('answer_feedback');
    answer_feedback.visible=false;
}

function end_game_setup(){

    let stats = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/stats.png"].texture);
    clearTimeout(gameTimer);
    app.stage.removeChildren();
    app.stage.addChild(stats);
    let successful = new PIXI.Text(correct_responses,{
        wordWrap: true,
        wordWrapWidth: 100,
        fontSize: 25,
        fontFamily: "Comic Sans MS",
        bold:true
    });
    let unsuccessful = new PIXI.Text(incorrect_responses,{
        wordWrap: true,
        wordWrapWidth: 100,
        fontSize: 25,
        fontFamily: "Comic Sans MS",
        bold: true
    });
    successful.x = app.stage.width/2 + 60;
    unsuccessful.x = app.stage.width/2 + 60;
    successful.y = app.stage.height/6 + 10;
    unsuccessful.y = app.stage.height * (2/6) - 20;
    quit_button_setup();
    app.stage.addChild(successful, unsuccessful);
}

function quit_button_setup(destination){
    let quit_button = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/quit_button.png"].texture);
    quit_button.x = app.stage.width * (9/10) + 20;
    quit_button.y = 10;
    quit_button.interactive = true;
    app.stage.addChild(quit_button);
    quit_button.on("mousedown",()=> {
        // TODO: run endsession logging protocol.
        app.stage.removeChildren();
        if (destination == "end_screen"){
            end_game_setup();
        }
        else{
            url = document.getElementById('menu_url');
            console.log(url);
            location.href = url;
        }
    });
}

//function setup_clear_order(){
//    let reset_button = app.stage.getChildByName("clear_order");
//    let reset_order = new PIXI.Text("CLEAR ORDER",{
//        wordWrap: true,
//        wordWrapWidth: 100,
//        fontSize: 20
//        });
//
//    reset_button.addChild(reset_order);
//    reset_order.x = 20;
//    reset_order.y = 20;
//    reset_button.x = app.stage.width * ( 4/5);
//    reset_button.y = app.stage.height * (3/5);
//    reset_button.beginFill(0xFFFFFF);
//    reset_button.lineStyle(4, 0x000000, 1);
//    reset_button.drawRect(10, 10, reset_order.width + 40, reset_order.height + 40 );
//    reset_button.endFill();
//    reset_button.interactive= true;
//    reset_button.on("mousedown", () =>{
//        let order = app.stage.getChildByName("order");
//        let children = order.children;
//        // TODO: Problem is here, not all children are removed/sent back to parent
//        // whether using a .map() call or for loop iterations, weird bug
//        children.map((child,index) => {
//            console.log(index);
//            order.removeChild(child);
//            return_order_member_to_parent(child);
//        });
//    });
//}

