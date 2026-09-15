import random
from flower import Flower
import matplotlib.pyplot as plt

def start_game():
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box') 

    # Random flower between 5 and 13 petals. The petal count's parity
    # (odd/even) is what decides "loves you" vs "loves you not" at the end.
    my_flower = Flower(random.randint(5, 13))
    my_flower.draw()

    ax.set_title("Loves me, loves me not\nClick the petals one by one!", fontsize=13)
    # Empty placeholder text that gets filled in with the result once the
    # last petal is plucked. Positioned in axes-fraction coordinates (0-1)
    # so it stays put regardless of the flower's data coordinates.
    result_text = ax.text(
        0.5, -0.08, "", transform=ax.transAxes,
        ha='center', va='top', fontsize=16, fontweight='bold'
    )
    
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
                print("You hit a petal!")
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
    
    plt.margins(0.05) 
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.show()

if __name__ == "__main__":
        start_game()