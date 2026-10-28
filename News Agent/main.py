
from agent import Agent

agent = Agent()

print('Enter quit to exit\n')


def run():
    while True:
        user_text = input('You: ')

        if user_text.lower().strip() == 'quit':
            break

        agent.run(user_text)


run()