from game import Game
import asyncio
import sys

def get_config_from_url():
    config = {'mode': 'medium', 'time': 'untimed'}
    try:
        # If running via Pygbag in browser, we can access the JS window object
        import js
        hash_val = js.window.location.hash
        if hash_val.startswith('#'):
            params = hash_val[1:].split('&')
            for p in params:
                if '=' in p:
                    k, v = p.split('=')
                    config[k] = v
    except ImportError:
        pass
    return config

if __name__ == "__main__":
    config = get_config_from_url()
    mode = config['mode']
    time_control = config['time']
    
    if mode == 'player':
        game = Game(play_vs_ai=False, time_control=time_control)
    else:
        game = Game(play_vs_ai=True, ai_difficulty=mode, time_control=time_control)
        
    asyncio.run(game.run())