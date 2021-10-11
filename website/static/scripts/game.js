var config = {
    type: Phaser.AUTO,
    width: 800,
    height: 600,
    parent: "game-area",
    physics: {
        default: 'arcade',
        arcade: {
            gravity: {y:300},
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    }
};

var game = new Phaser.Game(config);
var score = 1;
var scoreText;

// /static/assets/sky.png
function preload ()
{
    //preload assets
    this.load.image('sky', '/static/assets/sky.png');
    this.load.image('level', '/static/assets/platform.png');
    this.load.image('star', '/static/assets/star.png');
    this.load.spritesheet('player', '/static/assets/dude.png', { frameWidth: 32, frameHeight: 48 });
}

function create ()
{
    //background sky
    this.add.image(400, 300, 'sky');
    platforms = this.physics.add.staticGroup();

    platforms.create(400, 568, 'level').setScale(2).refreshBody();

    platforms.create(600, 400, 'level');
    platforms.create(50, 250, 'level');
    platforms.create(750, 220, 'level');

    //player physics
    player = this.physics.add.sprite(100, 450, 'player')

    player.setBounce(0.2);

    player.setCollideWorldBounds(true);

    player.body.setGravityY(300);

    this.physics.add.collider(player, platforms);

    this.anims.create({
        key: 'left',
        frames: this.anims.generateFrameNumbers('player', {start: 0, end: 3}),
        frameRate: 10,
        repeat: -1
    });
    this.anims.create({
        key: 'turn',
        frames: [ { key: 'player', frame: 4} ],
        frameRate: 20
    });
    this.anims.create({
        key: 'right',
        frames: this.anims.generateFrameNumbers('player', {start: 5, end: 8}),
        frameRate: 10,
        repeat: -1
    });

    keys = this.input.keyboard.createCursorKeys();

    //stars physics group (not static i dont think)
    stars = this.physics.add.group({
        key: 'star',
        repeat: 3,
        setXY: { x: 300, y: 0, stepX: 70 }
    });

    stars.children.iterate(function (child) {
        child.setBounceY(Phaser.Math.FloatBetween(0.4, 0.8));
        child.setCollideWorldBounds(true);
    });
    this.physics.add.collider(stars, platforms);
    this.physics.add.collider(stars, player);
    this.physics.add.collider(stars, stars);

    scoreText = this.add.text(16, 16, '',
    { fontSize: '32px', fill: '#030303' });

    win = this.physics.add.image(700, 0, 'star');
    this.physics.add.collider(win, platforms);

    this.physics.add.overlap(player, win, collectStar, null, this)
    function collectStar (player, win)
    {
        scoreText.setText('win');
    }
    // //score text
    // scoreText = this.add.text(16, 16, 'score: 1',
    // { fontSize: '32px', fill: '#030303' });
    // //platform physics (static group)
    // //detection between ground and stars
    // this.physics.add.collider(stars, platforms);
    // //detection overlap between player and stars
    // this.physics.add.overlap(player, stars, collectStar, null, this);
    // //stars collected
    // function collectStar(player, star) {
    //     star.disableBody(true, true);

    //     score += 10;
    //     scoreText.setText('Score: ' + score);
    // }
}


function update ()
{
    if(keys.left.isDown)
    {
        player.setVelocityX(-160);
        player.anims.play('left', true);

    }
    else if(keys.right.isDown)
    {
        player.setVelocityX(160);
        player.anims.play('right', true);
    }
    else
    {
        player.setVelocityX(0);
        player.anims.play('turn', true);
    }
    if (keys.up.isDown && player.body.touching.down)
    {
        player.setVelocityY(-450);
    }
}