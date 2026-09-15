import random
from flower import Flower
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def start_game():
    fig, ax = plt.subplots()
    # Leave some room at the bottom of the figure for the restart button.
    fig.subplots_adjust(bottom=0.2)

    # Placeholder - new_round() below fills these in for real.
    my_flower = None       
    result_text = None

    def new_round(event=None):
        """(Re)start the game: clear the plot and draw a fresh flower.
 
        Bound to both the "Restart" button and the 'r' key, and also
        called once at startup to draw the first flower.
        """
        nonlocal my_flower, result_text

        ax.clear()   # wipes out the old flower's petals/circle and any leftover text
        plt.sca(ax) # tell pyplot "ax is the current axes" before drawing
        ax.set_aspect('equal', adjustable='box')   # keep the flower circular, not stretched

        ax.set_title("Loves me, loves me not\nClick the petals one by one!", fontsize=13)
        plt.margins(0.05)
 
        # Empty placeholder text that gets filled in with the result once the
        # last petal is plucked. Positioned in axes-fraction coordinates (0-1)
        # so it stays put regardless of the flower's data coordinates.
        result_text = ax.text(
            0.5, -0.08, "", transform=ax.transAxes,
            ha='center', va='top', fontsize=16, fontweight='bold'
        )
 
        # Random flower between 5 and 13 petals. The petal count's parity
        # (odd/even) is what decides "loves you" vs "loves you not" at the end.
        my_flower = Flower(random.randint(5, 13))
        my_flower.draw()
        # Let matplotlib's own event loop decide the best moment to actually repaint the window.
        fig.canvas.draw_idle()

    def on_click(event):
        # Clicks outside the plot axes have no data coordinates - ignore them.
        if event.xdata is None or event.ydata is None:
            return
        point = [event.xdata, event.ydata]
        # If clicked on the center of the flower, do nothing.
        if my_flower.circle_path.contains_point(point):
            return
        # Check if the click is inside any of the petals.
        for artist in my_flower.petal_paths:
            inside, _ = artist.contains(event)
            # Remove the petal from both the plot and our tracking list.
            if inside:
                artist.remove()
                my_flower.petal_paths.remove(artist)
                fig.canvas.draw_idle()
            if not my_flower.petal_paths:
                # No petals left - reveal the result based on the
                # original petal count's parity (even = "not", odd = "yes").
                if my_flower.num_petals % 2 == 0:
                    result_text.set_text("Loves you not \N{WHITE HEART SUIT}")
                    result_text.set_color("gray")
                else:
                    result_text.set_text("Loves you \N{BLACK HEART SUIT}")
                    result_text.set_color("crimson")
                # End the game if all petals are removed.
                return

    def on_key(event):
        if event.key == 'r':
            new_round()

    # Small "Restart" button in its own axes at the bottom of the figure,
    # so it doesn't interfere with clicks on the flower itself.
    restart_ax = fig.add_axes([0.4, 0.02, 0.2, 0.07])
    restart_button = Button(restart_ax, 'Restart')
    restart_button.on_clicked(new_round)
    # Keep a strong reference alive
    fig.restart_button = restart_button

    # Wire up petal-click handler.
    fig.canvas.mpl_connect('button_press_event', on_click)   
    # Wire up 'r' key handler for restarting the game.
    fig.canvas.mpl_connect('key_press_event', on_key)

    # Draw the first flower.
    new_round()   

    plt.show()

if __name__ == "__main__":
        start_game()