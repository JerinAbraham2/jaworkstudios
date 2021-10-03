import { Scene } from 'phaser'

class PreloadScene extends Scene {
    constructor() {
        super('preload')
    }
    create() {
        this.input.on('pointerdown', () => this.scene.start('game'))
    }
    // watch this youtube tutorial when you are ready to have a restart button
    //https://www.youtube.com/watch?v=-BSz_FeWfkY
    //don't forget to put, type module. (and it also may not work fix it)

}