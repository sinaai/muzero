from helper import SharedStorage, MuZeroConfig, make_CartPole_config, ReplayBuffer
from self_play import run_selfplay, run_eval
from training import train_network


# MuZero training is split into two independent parts: Network training and
# self-play data generation.
# These two parts only communicate by transferring the latest network checkpoint
# from the training to the self-play, and the finished games from the self-play
# to the training.
def muzero(config: MuZeroConfig):

    storage = SharedStorage(config.new_network(), config.uniform_network(), config.new_optimizer())
    replay_buffer = ReplayBuffer(config)

    for loop in range(config.nb_training_loop):
        print("Training loop", loop)
        score_train = run_selfplay(config, storage, replay_buffer, config.nb_episodes)
        train_network(config, storage, replay_buffer, config.nb_epochs)

        print("Train score:", score_train)
        print("Eval score:", run_eval(config, storage, 5))
        print(f"MuZero played {config.nb_episodes * (loop + 1)} "
              f"episodes and trained for {config.nb_epochs * (loop + 1)} epochs.\n")
    return storage.latest_network()


if __name__ == '__main__':
    config = make_CartPole_config()
    muzero(config)