let app = new PIXI.Application({
        width: 800,
        height: 800,
        antialias: true,
        transparent: true,
        resolution: 1,
        sharedTicker: true,
        backgroundColor: 0xFFFFFF,
    }
);
app.renderer =  new PIXI.autoDetectRenderer(800, 800, {backgroundColor:0xFFFFFF, antialias: true});
document.body.appendChild(app.view);


PIXI.loader
    .add("/static/lettergame/image/buntemplate.png")
    .add("/static/lettergame/image/bottombuntemplate.png")
    .add("/static/lettergame/image/bunstationlabel.png")
    .add("/static/lettergame/image/meatstationlabel.png")
    .add("/static/lettergame/image/addonslabel.png")
    .add("/static/lettergame/image/meattemplate.png")
    .add("/static/lettergame/image/servelabel.png")
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
//    .add("/static/lettergame/image/nowloading.png")
    .add("/static/lettergame/image/check.png")
    .add("/static/lettergame/image/burgersmade.png")
    .add("/static/lettergame/image/stats.png")
    .add("/static/lettergame/image/goback.png")
    .add("/static/lettergame/image/x.png")
    .add("/static/lettergame/image/quit_button.png")
    .add("/static/lettergame/image/verbconj_feedback.png")
    .load(main);

function main(){
    level_setup();
}

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

    // 1. Load in the static assets:
    const bg_container = new PIXI.Container(name = "background");
    app.stage.addChild(bg_container);
    bg_setup(bg_container);
    const station_buttons_container = new PIXI.Container();
    station_buttons_container.name = "station_buttons"
    button_setup(station_buttons_container);
    app.stage.addChild(station_buttons_container);
    quit_button_setup("end_screen");

    const tray_container = new PIXI.Container();
    tray_container.name = "tray";
    tray_container.width = app.screen.width;
    tray_container.height = app.screen.height * (1 / 4);
    tray_setup(tray_container);
    app.stage.addChild(tray_container);

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

let game_performance = {"prefix": 0,
                   "suffix": 0,
                   "joiner": 0,
                   "verb": 0 };

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
                if (final_order['prefix'] == " "){
                    final_order['prefix']= "";
                }

                for (var order_item in final_order){
                    correct_components[order_item] = final_order[order_item] == conjugation_object[order_item];
                    game_performance[order_item] += (correct_components[order_item] ? 1 : 0)
                }
                console.log({"Correct comps" : correct_components});
//                order.map(child => {correct_components[child.type] = child.getChildAt(0).text == conjugation_object[child.type]})
//                order.map(child => {game_performance[child.type] += (correct_components[child.type] ? 1 : 0)});
                console.log(game_performance);
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
            console.log({'data':data});
            let order = app.stage.getChildByName("order");
            let prefix_array = document.getElementById("prefix_distractors");
            let suffix_array = document.getElementById("suffix_distractors");
            let verb_array = document.getElementById("verb_distractors");
            let verb = document.getElementById("verb");
            let conjugation_list = document.getElementById("conjugation_list");
            prefix_array.textContent = JSON.stringify(data.prefix_distractors);
            suffix_array.textContent = JSON.stringify(data.suffix_distractors);
            verb_array.textContent = JSON.stringify(data.verb_distractors);
            verb.textContent = JSON.stringify(data.verb);
            conjugation_list.textContent = JSON.stringify(data.conjugation_list);
            setTimeout(hide_feedback, 2000);
            views.bunstation.children.map(child => child.removeChildren());
            views.addonstation.removeChildren();
            views.burgerstation.removeChildren();
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
    let countdownclock = new PIXI.Text("Time remaining: " + (timeUntilEnd / 1000).toString(),             {
                fontFamily: 'Arial',
                fontSize: 28,
                fontWeight: 'bold',
            });
    app.stage.addChild(countdownclock);
    countdownclock.x = app.screen.width/2 - countdownclock.width/2;
    countdownclock.y = 10;

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
    let background = new PIXI.Graphics();
    background.name = "recipe_description"
    bg_container.addChild(background);
    let bgcolor = window.getComputedStyle(document.body).backgroundColor;
    background.beginFill(0xFFFFFF);
    background.drawRect(0,0, app.stage.width, app.stage.height);
    background.endFill();
    bg_container.addChild(background);

}

function button_setup(station_buttons_container) {
    let graphics = new PIXI.Graphics();
    graphics.beginFill(0xE84144);
    graphics.drawRect(0,0,190,30);
    graphics.endFill();
    const button_texture = app.renderer.generateTexture(graphics);
    let buttons = ["Prefix & Suffix", "Verb", "Add-ons", "Submit"]
    buttons = buttons.map((text,i) => new PIXI.Text(buttons[i],
            {
                fontFamily: 'Arial',
                fontSize: 16,
                fontWeight: 'bold',
                align: 'left',
                alpha: 1,
            }));
    buttons.forEach(text => text.anchor.set(0.5,0));
    let button_sprites = buttons.map(text => new PIXI.Sprite(button_texture));
    let buttons_names = ["bunstation", "burgerstation", "addonstation", "servestation"];
    let x_locs = [10, 210, 410, 610];
    button_sprites.forEach( (sprite, index) => {
                                       sprite.addChild(buttons[index]);
                                       sprite.interactive = true;
                                       sprite.x = x_locs[index];
                                       sprite.y = 760;
                                       sprite.name = buttons_names[index];
                                       sprite.children[0].x = sprite.width / 2;
                                       sprite.children[0].y += 5;
                                       station_buttons_container.addChild(sprite);
                                       });
}

function randomize_array(array){
    // Uses Fischer-Yates to shuffle array
    for(let i = array.length - 1; i > 0; i--){
      const j = Math.floor(Math.random() * i)
      const temp = array[i]
      array[i] = array[j]
      array[j] = temp
    }
    return array
}
function bun_section_setup(tb_container, bb_container) {
    let graphic = new PIXI.Graphics();

    let topbuntext = JSON.parse(document.getElementById("prefix_distractors").textContent);
    let bottombuntext = JSON.parse(document.getElementById("suffix_distractors").textContent);
    topbuntext = [...new Set(topbuntext)];
    bottombuntext = [...new Set(bottombuntext)];
    let top_buns = [];

    tb_container.x = app.screen.width * (1 / 4);
    tb_container.y = app.screen.height * (3.5 / 5);
    tb_container.pivot.x = tb_container.width / 2;
    tb_container.pivot.y = tb_container.height / 2;
    bb_container.x = app.screen.width * (3 / 4);
    bb_container.y = app.screen.height * (3.5 / 5);
    bb_container.pivot.x = bb_container.width / 2;
    bb_container.pivot.y = bb_container.height / 2;
    topbuntext = randomize_array(topbuntext);
    bottombuntext = randomize_array(bottombuntext);
    for (i = 0; i < Math.min(topbuntext.length,4); i++) {

        text_child = new PIXI.Text(topbuntext[i],
            {
                fontFamily: 'Arial',
                fontSize: 18,
                fontWeight: 'bold',
                align: 'center',
                alpha: 1,
            });
        text_child.anchor.set(.5, 0.5);
        width = 25 + text_child.width;
        graphic.beginFill(0xC0BDA5);
        graphic.drawRoundedRect(0,0, width, 40,5);
        graphic.endFill();
        const topbun = app.renderer.generateTexture(graphic);
        graphic.clear();
        const bun = new PIXI.Sprite(topbun);
        bun.anchor.set(0.5, 0.5);
        bun.x = bun.x_original =  (i % 2) * 90;
        bun.y = bun.y_original = Math.floor(i / 2) * 90;
        top_buns.push(bun);
        top_buns[i].type = "prefix";
        top_buns[i].buttonMode = true;
        top_buns[i].addChild(text_child);
        tb_container.addChild(top_buns[i]);
    }

    let bottom_buns = [];
    for (i = 0;  i < Math.min(bottombuntext.length,4); i++) {
        text_child = new PIXI.Text(bottombuntext[i],
            {
                fontFamily: 'Arial',
                fontSize: 18,
                fontWeight: 'bold',
                align: 'center',
                alpha: 1,
            });
        text_child.anchor.set(0.5, 0.5);
        width = 15 + text_child.width;
        graphic.beginFill(0xF39C6B);
        graphic.drawRoundedRect(0,0, width, 40, 5);
        graphic.endFill();
        const bottombun = app.renderer.generateTexture(graphic);
        graphic.clear();
        const bun = new PIXI.Sprite(bottombun);
        bun.anchor.set(0.5, 0.5);
        bun.x = bun.x_original = (i % 2) * 90;
        bun.y = bun.y_original = Math.floor(i / 2) * 90;
        bottom_buns.push(bun);
        bottom_buns[i].type = "suffix";
        bottom_buns[i].buttonMode = true;
        bottom_buns[i].addChild(text_child);
        bottom_buns[i].addChild(text_child)
        bb_container.addChild(bottom_buns[i]);
    }
    top_buns.map(create_drag_and_drop);
    bottom_buns.map(create_drag_and_drop);
    return {top_buns: top_buns, bottom_buns: bottom_buns}
}

function burger_section_setup(burger_container) {
    let graphic = new PIXI.Graphics();
    let burgtext = JSON.parse(document.getElementById("verb_distractors").textContent);
    const burger = new PIXI.Texture.from("/static/lettergame/image/meattemplate.png");
    let burgers = [];
    burgtext = randomize_array(burgtext);
    burger_container.x = app.screen.width * (1 / 4);
    burger_container.y = app.screen.height * (3.5 / 5);
    burger_container.pivot.x = burger_container.width / 2;
    burger_container.pivot.y = burger_container.height / 2;
    for (i = 0; i < Math.min(burgtext.length,4); i++) {
        text_child = new PIXI.Text(burgtext[i],
            {
                fontFamily: 'Arial',
                fontSize: 18,
                fontWeight: 'bold',
                align: 'center',
                alpha: 1,
            });
        text_child.anchor.set(.5, 0.6);
        width = 15 + text_child.width;
        graphic.beginFill(0x2B59C3);
        graphic.drawRoundedRect(0,0, width, 40,5);
        graphic.endFill();
        const burger = app.renderer.generateTexture(graphic);
        graphic.clear();
        const patty = new PIXI.Sprite(burger);
        patty.anchor.set(0.5, 0.5);
        patty.x = patty.x_original = (i % 2) * 275;
        patty.y = patty.y_original = Math.floor(i / 2) * 90;
        burgers.push(patty);
        burgers[i].type = "verb";
        burgers[i].buttonMode = true;
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
    let graphics = new PIXI.Graphics();
    for (let i = 0; i < 3; i++) {
        let index = i;
        graphics.beginFill(0xf27492);
        graphics.drawRoundedRect(0,0, 20, 40,5);
        graphics.endFill();
        const addon_text = app.renderer.generateTexture(graphics);
        graphics.clear();
        const addon = new PIXI.Sprite(addon_text);
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
//        addons[i].width = 34;
//        addons[i].height = 80;
        text_child = new PIXI.Text(addontext[i],
            {
                fontFamily: 'Arial',
                fontSize: 16,
                fontWeight: 'bold',
                align: 'center',
                alpha: 1,
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
            let ordering = ['prefix','verb','suffix','joiner'];
            let y_pos = [30, 70, 110];
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
    tray_container.x = app.screen.width/4;
    tray_container.y = app.screen.height * (2 / 5);
//    tray_container.pivot.x = app.screen.width / 2;
//    tray_container.pivot.y = app.screen.height / 2;
    let tray_graphic = new PIXI.Graphics();
    tray_graphic.beginFill(0xF2F2F2);
    tray_graphic.drawRoundedRect( 0, 0,  app.screen.width/2, app.screen.height * (1/4), 5);
    tray_graphic.endFill();
    tray_graphic.z
    tray_container.addChild(tray_graphic);
}

function post_order_to_backend(callback){

    let order = app.stage.getChildByName("order").children;
    let final_order = {"joiner": ""};
    order.map(child => final_order[child.type]=child.getChildAt(0).text);
//     For some reason PIXI.js replaces "" with " " for some reason
    if (final_order['prefix'] == " "){
        final_order['prefix'] = "";
    }
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
          'on_burger[]': final_order
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
    console.log({'conjugation': conjugation});
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
    let answer_feedback = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/verbconj_feedback.png"].texture);
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
    if(answer_feedback){
        answer_feedback.visible=false;
    }
}

function end_game_setup(){
    incorrect_responses = correct_responses + incorrect_responses == 0 ? 1 : incorrect_responses;
    let stats = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/stats.png"].texture);
    stats.alpha = 0;
    clearTimeout(gameTimer);
    app.stage.removeChildren();
    app.stage.addChild(stats);
    let successful = new PIXI.Text(correct_responses.toString() + "  CONJUGATIONS CORRECT!!" ,{
        fontSize: 25,
        fontFamily: "Arial",
        bold:true
    });
    let unsuccessful = new PIXI.Text(incorrect_responses.toString() + "  INCORRECT CONJUGATIONS" ,{
        fontSize: 25,
        fontFamily: "Arial",
        bold: true
    });
    let game_over = new PIXI.Text("GAME OVER",{
        fontSize: 32,
        fontFamily: "Arial",
        bold: true
    });
    let performance_texts = {};
    let performance_ratios = {};
    let i = 0;
    let graphics = new PIXI.Graphics();
    total_questions = correct_responses+incorrect_responses;
    for (var comp in game_performance) {
        percent_correct = game_performance[comp]/total_questions;
        performance_texts[comp] = new PIXI.Text(comp.toUpperCase(),{fontSize: 25,
                                                                    fontFamily: "Arial",
                                                                    bold: true});
        performance_ratios[comp] = new PIXI.Text(game_performance[comp].toString() + "/" + total_questions.toString(),{fontSize: 25,
                                                                    fontFamily: "Arial",
                                                                    bold: true});
        y_offset = app.stage.height * (3/6) + i * 50 ;
        graphics.beginFill(0x031b4d);
        // Negative fill
        graphics.drawRoundedRect(app.stage.width * 1/3, y_offset, app.stage.width * 1/3, 40, 5 );
        graphics.endFill();
        if (percent_correct > 0){
            graphics.beginFill(0x0bb763);
            graphics.drawRoundedRect(app.stage.width * 1/3, y_offset, app.stage.width * 1/3 * percent_correct, 40, 5 );
            graphics.endFill();
        }
        performance_texts[comp].x = app.stage.width * 1/3 - performance_texts[comp].width - 5 ;
        performance_texts[comp].y = y_offset + 5;
        performance_ratios[comp].x = app.stage.width * 2/3 + 5
        performance_ratios[comp].y = y_offset + 5;
        i += 1;
        app.stage.addChild(performance_texts[comp],performance_ratios[comp],graphics);
    }

    successful.x = app.stage.width/2 - successful.width/2;
    unsuccessful.x = app.stage.width/2 - unsuccessful.width/2;
    successful.y = app.stage.height/6 + 10;
    unsuccessful.y = app.stage.height * (2/6) - 20;
    game_over.x = app.stage.width/2 - game_over.width/2;
    game_over.y = 20;
    quit_button_setup();
    app.stage.addChild(successful, unsuccessful, game_over);
}

function quit_button_setup(destination){
    let quit_button = new PIXI.Sprite(PIXI.loader.resources["/static/lettergame/image/quit_button.png"].texture);
    quit_button.x = app.stage.width * (9/10) + 20;
    quit_button.y = 10;
    quit_button.interactive = true;
    app.stage.addChild(quit_button);
    quit_button.on("mousedown",()=> {
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