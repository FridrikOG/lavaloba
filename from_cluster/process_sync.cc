#include <stdio.h>
#include <mpi.h>

// Simple program with a client/server topology to run processes
// in parallel. The server process will execute a control path
// and the client processes will execute a common parallel path (thread).
//
// Typically in distributed systems, this would be written as two
// separate programs. (See TSAM)

#define NO_PROCESSES 3

int main(int argc, char *argv[])
{
    clock_t begin = clock();
    MPI_Status status;
    int my_id, ierr, num_procs;
    int server_id;
    int range[NO_PROCESSES];

    ierr = MPI_Init(&argc, &argv);

    server_id = 0;

    /* find out MY process ID, and how many processes were started. */

    ierr = MPI_Comm_rank(MPI_COMM_WORLD, &my_id);
    ierr = MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

    if(my_id == 0)
        printf("Server id (rank) is: %d\n", my_id);
    else
        printf("Client id (rank) is: %d\n", my_id);

    // Prepare program data to send to clients. MPI_Send/MPI_Recv specify
    // the datatype which is used

    range[0] = 0;
    range[1] = 0xffff/NO_PROCESSES;


    // Determine if this process is the server (root) process
    // Could pick any number here, as long as it is a rank of one of the
    // processes.
     if(my_id == server_id)
    {
       printf("Hello I am the server before sync: %d\n", my_id);
    //    MPI_Barrier(MPI_COMM_WORLD);
    //    printf("Hello I am the server after sync: %d\n", my_id);
       for(int i = 1; i < NO_PROCESSES; i++)
       {
           range[0] = 1000 * (i - 1);
           range[1] = range[0] + 1000;
           int rank_recv;
           MPI_Send(range, 2, MPI_INT, i, 0, MPI_COMM_WORLD);
           printf("Server: sent to client %d\n", i);
           MPI_Recv((void *)&rank_recv, 1, MPI_INT, i, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE); // recv from all clients
        //    MPI_Recv(i, NO_PROCESSES, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
           printf("Server: received from client %d\n", rank_recv);
       }
    }
    else
    // Slave process, receive the array range to calculate, and send
    // it back to the server when finished.
    {
       printf("Hello I am process: %d\n", my_id);
       MPI_Recv(range, NO_PROCESSES, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
       printf("Client id: %d Received: %d %d\n",my_id, range[0], range[1]);
       // void* data, count, MPI_Datatype, destination, tag, MPI_COMM
       MPI_Send((void *)&my_id, 1, MPI_INT, 0, 0, MPI_COMM_WORLD);   // sends to server
    }
   
    MPI_Finalize();
}