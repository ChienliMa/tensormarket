import tensorflow as tf

from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

export_dir =  "/tmp/model10.ckpt"
def train_and_save():
    builder = tf.saved_model.builder.SavedModelBuilder(export_dir)
    with tf.Session() as sess:
        
        x = tf.placeholder(tf.float32, [None, 784], name = "input_data")
        W = tf.Variable(tf.zeros([784, 10]), name = 'weight')
        b = tf.Variable(tf.zeros([10]), name = "bias")
        y = tf.nn.softmax(tf.matmul(x, W) + b, name = "output_prob")
        y_ = tf.placeholder(tf.float32, [None, 10], name = "expected_prob")

        cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))

        train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

        tf.global_variables_initializer().run()
        for _ in range(1000):
            batch_xs, batch_ys = mnist.train.next_batch(100)
            sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

        inputs = {'input': tf.saved_model.utils.build_tensor_info(x)}
        outputs = {'output' : tf.saved_model.utils.build_tensor_info(y)}
        signature = tf.saved_model.signature_def_utils.build_signature_def(inputs, outputs, 'main')

        builder.add_meta_graph_and_variables(sess, 
                                            ['logistic_mnist_graph'], 
                                            {'main_signature':signature})

        builder.save()
        print("Model saved in file: %s" % export_dir)

def load_and_estimate():
    with tf.Session(graph=tf.Graph()) as sess:
        meta_graph_def = tf.saved_model.loader.load(sess, ['logistic_mnist_graph'], export_dir)
        signature = meta_graph_def.signature_def

        x_tensor_name = signature['main_signature'].inputs['input'].name
        y_tensor_name = signature['main_signature'].outputs['output'].name

        x = sess.graph.get_tensor_by_name(x_tensor_name)
        y = sess.graph.get_tensor_by_name(y_tensor_name)

        y_ = tf.placeholder(tf.float32, [None, 10], name = "label")
        correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
        print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))
if __name__ == "__main__":
    train_and_save()
    load_and_estimate()
