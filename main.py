from game import Game
import asyncio
import sys

def get_mode_from_url():
    try:
        # If running via Pygbag in browser, we can access the JS window object
        import js
        hash_val = js.window.location.hash
        if hash_val.startswith('#mode='):
            return hash_val.split('=')[1]
    except ImportError:
        pass
    # Default if running locally via normal Python
    return 'medium'

if __name__ == "__main__":
    mode = get_mode_from_url()
    
    if mode == 'player':
        game = Game(play_vs_ai=False)
    else:
        game = Game(play_vs_ai=True, ai_difficulty=mode)
        
    asyncio.run(game.run())