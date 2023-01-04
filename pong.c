#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/pio.h"
#include "hardware/dma.h"
#include "hardware/uart.h"
#include "hardware/irq.h"

#include "hsync.pio.h"
#include "vsync.pio.h"
#include "rgb.pio.h"

#define H_ACTIVE   655
#define V_ACTIVE   479
#define RGB_ACTIVE 319
// #define RGB_ACTIVE 639 // change to this if 1 pixel/byte

// Length of the pixel array, and number of DMA transfers
#define TXCOUNT 153600 // Total pixels/2 (since we have 2 pixels per byte)

// Pixel color array that is DMA's to the PIO machines and
// a pointer to the ADDRESS of this color array.
// Note that this array is automatically initialized to all 0's (black)
unsigned char vga_data_array[TXCOUNT];
char * address_pointer = &vga_data_array[0] ;

// Give the I/O pins that we're using some names that make sense
#define HSYNC     16
#define VSYNC     17
#define RED_PIN   18
#define GREEN_PIN 19
#define BLUE_PIN  20

// We can only produce 8 colors, so let's give them readable names
#define BLACK   0
#define RED     1
#define GREEN   2
#define YELLOW  3
#define BLUE    4
#define MAGENTA 5
#define CYAN    6
#define WHITE   7


// A function for drawing a pixel with a specified color.
// Note that because information is passed to the PIO state machines through
// a DMA channel, we only need to modify the contents of the array and the
// pixels will be automatically updated on the screen.
void drawPixel(int x, int y, char color) {
    // Range checks
    if (x > 639) x = 639 ;
    if (x < 0) x = 0 ;
    if (y < 0) y = 0 ;
    if (y > 479) y = 479 ;

    // Which pixel is it?
    int pixel = ((640 * y) + x) ;

    // Is this pixel stored in the first 3 bits
    // of the vga data array index, or the second
    // 3 bits? Check, then mask.
    if (pixel & 1) {
        char mask = 0x0f;
        char other = vga_data_array[pixel>>1] & mask;
        vga_data_array[pixel>>1] = other | (color << 3);
    }
    else {
        char mask = 0xf0;
        char other = vga_data_array[pixel>>1] & mask;
        vga_data_array[pixel>>1] = color | other;
    }
}
////////////////////////////////////////////////////////////////////////////////////////////////////
/////////////// Stuff for Mandelbrot ///////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////////////////////
// Fixed point data type
typedef signed int fix28 ;
#define multfix28(a,b) ((fix28)(((( signed long long)(a))*(( signed long long)(b)))>>28)) 
#define float2fix28(a) ((fix28)((a)*268435456.0f)) // 2^28
#define fix2float28(a) ((float)(a)/268435456.0f) 
#define int2fix28(a) ((a)<<28)
// the fixed point value 4
#define FOURfix28 0x40000000 
#define SIXTEENTHfix28 0x01000000
#define ONEfix28 0x10000000

// Maximum number of iterations
#define max_count 1000

// Mandelbrot values
fix28 Zre, Zim, Cre, Cim ;
fix28 Zre_sq, Zim_sq ;

int i, j, count, total_count ;

fix28 x[640] ;
fix28 y[480] ;

char color = WHITE;

void on_uart_rx() {
    char ch = uart_getc(uart0);
    if (uart_is_writable(uart0)) { uart_putc(uart0, ch + 1); }
}

int main() {
    stdio_init_all();

    PIO pio = pio0;

    uint hsync_offset = pio_add_program(pio, &hsync_program);
    uint vsync_offset = pio_add_program(pio, &vsync_program);
    uint rgb_offset = pio_add_program(pio, &rgb_program);

    uint hsync_sm = 0;
    uint vsync_sm = 1;
    uint rgb_sm = 2;

    hsync_program_init(pio, hsync_sm, hsync_offset, HSYNC);
    vsync_program_init(pio, vsync_sm, vsync_offset, VSYNC);
    rgb_program_init(pio, rgb_sm, rgb_offset, RED_PIN);


    /////////////////////////////////////////////////////////////////////////////////////////////////////
    // ===========================-== DMA Data Channels =================================================
    /////////////////////////////////////////////////////////////////////////////////////////////////////

    // DMA channels - 0 sends color data, 1 reconfigures and restarts 0
    int rgb_chan_0 = 0;
    int rgb_chan_1 = 1;

    // Channel Zero (sends color data to PIO VGA machine)
    dma_channel_config c0 = dma_channel_get_default_config(rgb_chan_0);  // default configs
    channel_config_set_transfer_data_size(&c0, DMA_SIZE_8);              // 8-bit txfers
    channel_config_set_read_increment(&c0, true);                        // yes read incrementing
    channel_config_set_write_increment(&c0, false);                      // no write incrementing
    channel_config_set_dreq(&c0, DREQ_PIO0_TX2) ;                        // DREQ_PIO0_TX2 pacing (FIFO)
    channel_config_set_chain_to(&c0, rgb_chan_1);                        // chain to other channel

    dma_channel_configure(
        rgb_chan_0,
        &c0,
        &pio->txf[rgb_sm],
        &vga_data_array,
        TXCOUNT,
        false
    );

    dma_channel_config c1 = dma_channel_get_default_config(rgb_chan_1);
    channel_config_set_transfer_data_size(&c1, DMA_SIZE_32);
    channel_config_set_read_increment(&c1, false);
    channel_config_set_write_increment(&c1, false);
    channel_config_set_chain_to(&c1, rgb_chan_0);

    dma_channel_configure(
        rgb_chan_1,
        &c1,
        &dma_hw->ch[rgb_chan_0].read_addr,
        &address_pointer,
        1,
        false
    );

    pio_sm_put_blocking(pio, hsync_sm, H_ACTIVE);
    pio_sm_put_blocking(pio, vsync_sm, V_ACTIVE);
    pio_sm_put_blocking(pio, rgb_sm, RGB_ACTIVE);


    pio_enable_sm_mask_in_sync(pio, ((1u << hsync_sm) | (1u << vsync_sm) | (1u << rgb_sm)));

    dma_start_channel_mask((1u << rgb_chan_0)) ;


    uint64_t begin_time ;
    uint64_t end_time ;
    int a=0, b=0, c=0;
    while (true) {
        scanf("%d %d %d", &a, &b, &c);
        printf("\n");
        for (i=0; i<640; i++) {
            for (j=0; j<480; j++) {
                if ((i >= 20 && i <= 60) && (j > a && j < a + 120) ||
                    (i >= 580 && i < 620) && (j > b && j < b + 120)) {
                    drawPixel(i, j, color);
                } else {
                    drawPixel(i, j, BLACK);
                }
            }
        }
        a++;
        if (a > 40) { a = 20; }
    }
}
