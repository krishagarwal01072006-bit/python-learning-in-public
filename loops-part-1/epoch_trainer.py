# epoch_trainer.py
# Day 5 project: train a (very fake) AI model, one epoch at a time.
# Change epochs, then rerun. Watch the loss drop every loop.

epochs = 5
loss = 100  # every model starts out terrible

for epoch in range(1, epochs + 1):
    loss = loss - 15  # each epoch learns a little
    print("epoch", epoch, "- loss:", loss)

print("Training done! Loss went from 100 down to", loss)
print("Real models train for thousands of epochs. Same loop, bigger ambition.")
